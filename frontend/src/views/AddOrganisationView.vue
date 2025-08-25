<template>
  <PageHeading pageTitle="Add Organisation" />
  <div class="container">
    <div class="section">
      <router-link to="/organisations">Go back to Organisations List</router-link>
      <div class="field pt-5">
        <o-field
          class="label"
          label="Entity Name:"
          :message="nameValidation.nameClasses === 'is-danger' ? 'Please enter the entity name' : ''">
          <o-input
            class="input"
            :class="this.nameValidation.nameClasses"
            v-model="name"
            maxlength="200"
            @blur="() => validateName(this.name)">
          </o-input>
        </o-field>
      </div>
      <div class="field">
        <o-field
          class="label"
          label="ABN:"
          :message="abnValidation.abnClasses === 'is-danger' ? 'Please enter a valid ABN' : ''">
          <o-input
            class="input"
            :class="this.abnValidation.abnClasses"
            v-model="abn"
            @blur="() => validateABN(this.abn)">
          </o-input>
        </o-field>
      </div>
      <div class="field">
        <o-field
          class="label"
          :message="emailValidation.emailClasses === 'is-danger' ? 'Please enter a valid email address' : ''"
          label="Email:">
          <o-input
            class="input"
            :class="this.emailValidation.emailClasses"
            @blur="() => validateEmail(this.email)"
            v-model="email">
          </o-input>
        </o-field>
        <p v-if="emailError" class="help is-danger">{{ emailError }}</p>
      </div>
      <div class="field is-grouped">
        <o-button
          :disabled="canSubmitForm || this.loading"
          :class="{ 'is-loading': this.loading }"
          class="button"
          @click="this.createOrganisation"
          >Add</o-button
        >
      </div>
    </div>
  </div>
</template>

<script>
import { createOrganisationAPI } from '../api/api.ts';
import { abnValidator, emailValidator, nameValidator } from '../helpers/helpers';
import { useProgrammatic } from '@oruga-ui/oruga-next';
import PageHeading from '@/components/PageHeading.vue';
import { useUserDataStore } from '@/store';

export default {
  name: 'AddOrganisationView',
  components: { PageHeading },
  data() {
    return {
      name: '',
      nameValidation: {
        valid: false,
        nameClasses: '',
      },
      abn: '',
      abnValidation: {
        valid: false,
        abnClasses: '',
      },
      email: '',
      emailValidation: {
        valid: false,
        emailClasses: '',
      },
      emailError: '',
      notification: null,
      loading: false,
    };
  },
  watch: {},
  computed: {
    canSubmitForm() {
      return !(this.abnValidation.valid && this.nameValidation.valid && this.emailValidation.valid);
    },
  },
  methods: {
    validateName(name) {
      this.nameValidation = nameValidator(name);
    },
    validateABN(abn) {
      this.abnValidation = abnValidator(abn);
    },
    validateEmail(email) {
      const userStore = useUserDataStore();
      this.emailValidation = emailValidator(email);
      if (email === userStore.email) {
        this.emailValidation.valid = false;
        this.emailValidation.emailClasses = 'is-danger';
        this.emailError = 'Organisation email cannot be the same as your work email.';
      } else {
        this.emailError = '';
      }
    },
    async createOrganisation() {
      const { oruga } = useProgrammatic();
      this.loading = true;
      this.notification = await createOrganisationAPI(this.name, this.abn, this.email);
      this.loading = false;
      if (this.notification) {
        oruga.notification.open({
          message: this.notification[0],
          position: 'top',
          variant: this.notification[1] ? 'success' : 'danger',
          closable: true,
        });
        if (this.notification[1]) {
          return this.clearFields();
        }
      }
    },
    clearFields() {
      this.name = '';
      this.nameValidation = {
        valid: false,
        nameClasses: '',
      };
      this.abn = '';
      this.abnValidation = {
        valid: false,
        abnClasses: '',
      };
      this.email = '';
      this.emailValidation = {
        valid: false,
        emailClasses: '',
      };
    },
  },
};
</script>

<style scoped></style>
