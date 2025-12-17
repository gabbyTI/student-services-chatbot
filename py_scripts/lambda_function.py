import json
import boto3
import uuid
import logging
from datetime import datetime

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')

# DynamoDB tables
courses_table = dynamodb.Table('Courses')
registrations_table = dynamodb.Table('Registrations')

# -------------------------
#   MAIN ROUTER
# -------------------------
def lambda_handler(event, context):
    logger.info(f"Lambda handler invoked with event: {json.dumps(event)}")
    intent = event['sessionState']['intent']['name']
    logger.info(f"Processing intent: {intent}")

    if intent == 'RegisterCourseIntent':
        return handle_register_course(event)

    elif intent == 'LibraryHoursIntent':
        return handle_library_hours(event)

    elif intent == 'ViewRegisteredCoursesIntent':
        return handle_view_courses(event)

    elif intent == 'UnregisterCourseIntent':
        return handle_unregister_course(event)

    elif intent == 'GetAvailableCoursesIntent':
        return handle_available_courses(event)
    
    elif intent == 'FallbackIntent':
        return handle_fallback(event)

    else:
        return close_intent(event, 'Fulfilled', "I'm not sure how to handle that yet.")

# -------------------------
#   GET AVAILABLE COURSES
# -------------------------
def handle_available_courses(event):
    logger.info("Handling GetAvailableCoursesIntent")
    response = courses_table.scan()
    items = response.get('Items', [])
    logger.info(f"Found {len(items)} available courses")

    if not items:
        logger.warning("No courses found in database")
        return close_intent(event, 'Fulfilled', "No courses are currently available.")

    message = "📚 Available Courses:\n\n"
    # tootal courses
    message += f"Total: {len(items)}\n\n"

    for c in items:
        message += f"- {c['course_name']} ({c['course_id']})\n"
        message += f"  Instructor: {c.get('instructor', 'TBA')}\n"
        message += f"  Schedule: {c.get('schedule', 'TBA')}\n"
        message += f"  Capacity: {c.get('enrolled_count', 0)}/{c.get('capacity', 0)}\n\n"

    return close_intent(event, 'Fulfilled', message)

# -------------------------
#   REGISTER COURSE
# -------------------------
def handle_register_course(event):
    logger.info("Handling RegisterCourseIntent")
    session_attributes = event['sessionState'].get('sessionAttributes', {})
    student_id = session_attributes.get('student_id')
    student_name = session_attributes.get('name', 'Student')
    logger.info(f"Student ID: {student_id}, Name: {student_name}")

    if not student_id:
        logger.error("Missing student_id in session attributes")
        return close_intent(event, "Failed", "I couldn’t verify your student identity.")

    slots = event['sessionState']['intent']['slots']
    course_slot = slots.get('CourseID')

    if not course_slot or not course_slot.get('value'):
        return elicit_slot(event, 'CourseID', 'Which course would you like to register for?')

    course_id = course_slot['value']['interpretedValue']
    logger.info(f"Attempting to register student {student_id} for course {course_id}")

    try:
        course_response = courses_table.get_item(Key={'course_id': course_id})
        if 'Item' not in course_response:
            logger.warning(f"Course {course_id} not found in database")
            return close_intent(event, 'Failed', f"Course {course_id} does not exist.")

        course = course_response['Item']
        logger.info(f"Course found: {course.get('course_name')}, Capacity: {course['enrolled_count']}/{course['capacity']}")

        if course['enrolled_count'] >= course['capacity']:
            logger.warning(f"Course {course_id} is full")
            return close_intent(event, 'Failed', f"{course['course_name']} is full.")

        existing = registrations_table.query(
            IndexName='student-index',
            KeyConditionExpression='student_id = :sid',
            ExpressionAttributeValues={':sid': student_id}
        )
        already_registered = any(r['course_id'] == course_id for r in existing.get('Items', []))
        if already_registered:
            logger.warning(f"Student {student_id} already registered for {course_id}")
            return close_intent(event, 'Failed', f"You are already registered for {course['course_name']}.")

        # Register student
        registration_id = str(uuid.uuid4())
        logger.info(f"Creating registration {registration_id} for student {student_id}, course {course_id}")
        registrations_table.put_item(Item={
            'registration_id': registration_id,
            'student_id': student_id,
            'course_id': course_id,
            'status': 'enrolled',
            'registration_date': datetime.now().strftime('%Y-%m-%d')
        })

        # Increase enrollment count
        courses_table.update_item(
            Key={'course_id': course_id},
            UpdateExpression='SET enrolled_count = enrolled_count + :v',
            ExpressionAttributeValues={':v': 1}
        )
        
        logger.info(f"Successfully registered student {student_id} for course {course_id}")

        success = (
            f"🎉 Success, {student_name}! You're now registered for {course['course_name']} ({course_id}).\n\n"
            f"📅 Schedule: {course.get('schedule', 'TBA')}\n"
            f"👨‍🏫 Instructor: {course.get('instructor', 'TBA')}\n"
            f"🏫 Room: {course.get('room', 'TBA')}\n"
            f"💳 Credits: {course.get('credits', 'N/A')}\n\n"
            f"Let me know if you want to view or drop a course!"
        )
        return close_intent(event, 'Fulfilled', success)

    except Exception as e:
        logger.error(f"Error during registration: {str(e)}", exc_info=True)
        return close_intent(event, 'Failed', "Something went wrong while registering.")

# -------------------------
#   VIEW REGISTERED COURSES
# -------------------------
def handle_view_courses(event):
    logger.info("Handling ViewRegisteredCoursesIntent")
    session_attributes = event['sessionState'].get('sessionAttributes', {})
    student_id = session_attributes.get('student_id')
    student_name = session_attributes.get('name', 'Student')
    logger.info(f"Fetching courses for student {student_id}")

    if not student_id:
        logger.error("Missing student_id in session attributes")
        return close_intent(event, "Failed", "I couldn’t verify your student identity.")

    registration_list = registrations_table.query(
        IndexName='student-index',
        KeyConditionExpression='student_id = :sid',
        ExpressionAttributeValues={':sid': student_id}
    ).get('Items', [])
    
    logger.info(f"Student {student_id} has {len(registration_list)} registered courses")

    if not registration_list:
        return close_intent(event, "Fulfilled", f"{student_name}, you are not registered for any courses yet.")

    msg = f"Here are your registered courses, {student_name}:\n\n"
    for reg in registration_list:
        course = courses_table.get_item(Key={'course_id': reg['course_id']}).get('Item', {})
        msg += f"- {course.get('course_name', reg['course_id'])} ({reg['course_id']})\n"
        msg += f"  Schedule: {course.get('schedule', 'TBA')}\n"
        msg += f"  Room: {course.get('room', 'TBA')}\n\n"

    return close_intent(event, "Fulfilled", msg)

# -------------------------
#   UNREGISTER COURSE
# -------------------------
def handle_unregister_course(event):
    logger.info("Handling UnregisterCourseIntent")
    session_attributes = event['sessionState'].get('sessionAttributes', {})
    student_id = session_attributes.get('student_id')
    if not student_id:
        logger.error("Missing student_id in session attributes")
        return close_intent(event, "Failed", "I couldn’t verify your student identity.")

    slots = event['sessionState']['intent']['slots']
    course_slot = slots.get('CourseID')
    if not course_slot:
        return elicit_slot(event, 'CourseID', 'Which course would you like to drop?')

    course_id = course_slot['value']['interpretedValue']
    logger.info(f"Attempting to unregister student {student_id} from course {course_id}")

    regs = registrations_table.query(
        IndexName='student-index',
        KeyConditionExpression='student_id = :sid',
        ExpressionAttributeValues={':sid': student_id}
    ).get('Items', [])

    reg_obj = next((r for r in regs if r['course_id'] == course_id), None)
    if not reg_obj:
        logger.warning(f"Student {student_id} not registered for course {course_id}")
        return close_intent(event, 'Failed', f"You are not registered for {course_id}.")

    logger.info(f"Deleting registration {reg_obj['registration_id']}")
    registrations_table.delete_item(Key={'registration_id': reg_obj['registration_id']})

    courses_table.update_item(
        Key={'course_id': course_id},
        UpdateExpression='SET enrolled_count = enrolled_count - :v',
        ExpressionAttributeValues={':v': 1}
    )
    
    logger.info(f"Successfully unregistered student {student_id} from course {course_id}")

    return close_intent(event, 'Fulfilled', f"✔ You have successfully dropped {course_id}.")

# -------------------------
#   LIBRARY HOURS
# -------------------------
def handle_library_hours(event):
    logger.info("Handling LibraryHoursIntent")
    message = (
        "📚 Library Hours:\n"
        "Mon–Thu: 8AM–10PM\n"
        "Fri: 8AM–6PM\n"
        "Sat: 10AM–5PM\n"
        "Sun: 12PM–8PM\n"
        "\nDuring finals week: OPEN 24/7!"
    )
    return close_intent(event, 'Fulfilled', message)

# -------------------------
#   FALLBACK INTENT
# -------------------------
def handle_fallback(event):
    logger.info("Handling FallbackIntent")
    message = (
        "🤔 I didn't understand that. I can help you with:\n"
        "• Registering for courses\n"
        "• Viewing your courses\n"
        "• Dropping a course\n"
        "• Checking library hours\n\n"
        "What would you like to do?"
    )
    return close_intent(event, 'Fulfilled', message)

# -------------------------
#   HELPERS
# -------------------------
def close_intent(event, state, message):
    return {
        'sessionState': {
            'dialogAction': {'type': 'Close'},
            'intent': {
                'name': event['sessionState']['intent']['name'],
                'state': state
            },
            'sessionAttributes': event['sessionState'].get('sessionAttributes', {})
        },
        'messages': [{'contentType': 'PlainText', 'content': message}]
    }

def elicit_slot(event, slot, message):
    return {
        'sessionState': {
            'dialogAction': {'type': 'ElicitSlot', 'slotToElicit': slot},
            'intent': event['sessionState']['intent']
        },
        'messages': [{'contentType': 'PlainText', 'content': message}]
    }
