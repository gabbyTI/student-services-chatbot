export const awsConfig = {
  Auth: {
    Cognito: {
      userPoolId: 'us-east-1_9IFQ0LPqU',
      userPoolClientId: '3i3v4q1j9tog9cel2rq00mstm',
      loginWith: {
        email: true
      },
      signUpVerificationMethod: 'code',
      userAttributes: {
        email: {
          required: true
        },
        name: {
          required: true
        }
      },
      passwordFormat: {
        minLength: 8,
        requireLowercase: true,
        requireUppercase: true,
        requireNumbers: true,
        requireSpecialCharacters: true
      }
    }
  }
};