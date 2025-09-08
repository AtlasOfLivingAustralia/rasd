import type { AxiosError } from 'axios';
import { logOutAndClearUserData, useUserDataStore } from '@/store';
import { notifyError } from '@/helpers/helpers';
import router from '@/router';

// Intercept authentication error (401 and 403), notify user and redirect to login page.
// The main use case of this interceptor is to catch auth token (idToken) that has expired (401)
function catchAuthError(error: AxiosError): Promise<AxiosError> {
  const statusCode = error.response?.status;
  const url = error.config?.url;
  if ((statusCode === 401 || statusCode === 403) && !url?.includes('/auth/login')) {
    const user = useUserDataStore();
    let errorMessage: string;
    if (user.isLoggedIn) {
      errorMessage = 'Your session has expired. You need to login again.';
      logOutAndClearUserData();
    } else {
      errorMessage = 'You must be logged-in to perform this action.';
    }
    router.push('login');
    notifyError(errorMessage);
  }
  return Promise.reject(error);
}

export { catchAuthError };
