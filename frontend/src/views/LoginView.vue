<template>
  <PageHeading pageTitle="Login as an existing user" />
  <div class="container">
    <div class="section">
      <o-field label="Username:">
        <o-input
          type="email"
          id="username"
          v-model="username"
          placeholder="Your work email address"
          maxlength="200"></o-input>
      </o-field>
      <o-field label="Password:" class="pt-4">
        <o-input type="password" id="password" v-model="password"></o-input>
      </o-field>
      <div class="mt-4 mb-4 container is-flex is-justify-content-space-between is-align-items-center">
        <o-button
          class="button"
          :class="{ 'is-loading': isLoading }"
          :disabled="isLoading"
          variant="primary"
          @click="login()">
          Log in
        </o-button>
        <router-link class="mt-4" to="forgot-password">Forgot password</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import PageHeading from '../components/PageHeading.vue';
import { useProgrammatic } from '@oruga-ui/oruga-next';
import { loginAPI } from '@/api/api';

export default {
  components: {
    PageHeading,
  },
  props: {
    from: {
      type: String,
    },
  },
  data() {
    return {
      username: '',
      password: '',
      isLoading: false,
    };
  },
  methods: {
    async login() {
      const { oruga } = useProgrammatic();
      this.isLoading = true;
      this.notification = await loginAPI(this.username, this.password);
      console.log('Login response:', this.notification);
      this.isLoading = false;
      if (this.notification[1] === true) {
        this.$router.push(this.from || '/tools');
      } else if (this.notification[0] === 'PASSWORD_EXPIRED') {
        oruga.notification.open({
          variant: 'warning',
          message: 'Your password has expired. Redirecting to password reset...',
          position: 'top',
          closable: false,
          duration: 2000,
        });
        setTimeout(() => {
          this.$router.push('/forgot-password');
        }, 2000);
      } else {
        oruga.notification.open({
          variant: 'danger',
          message: this.notification[0],
          position: 'top',
          closable: true,
          duration: 3000,
        });
        this.clearFields();
      }
    },
    clearFields() {
      this.username = '';
      this.password = '';
    },
  },
};
</script>

<style scoped></style>
