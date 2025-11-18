export const awsConfig = {
  Auth: {
    Cognito: {
      userPoolId: 'us-east-1_9IFQ0LPqU',
      userPoolClientId: '3i3v4q1j9tog9cel2rq00mstm',
      identityPoolId: "us-east-1:1f4b6e1d-efb5-49f8-a70f-d0f6c2cf6023",
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

export const lexConfig = {
  botId: 'EIGIS2NJTN',
  botAliasId: 'TSTALIASID',
  localeId: 'en_US',
  region: 'us-east-1'
};