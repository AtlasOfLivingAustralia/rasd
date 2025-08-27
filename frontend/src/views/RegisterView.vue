<template>
  <PageHeadingWithDescription pageTitle="Registration" :page-description="subtitle" />
  <div class="container">
    <div class="section">
      <div class="field">
        <o-field class="label" label="* First Name:">
          <o-input
            class="input"
            v-model="firstName"
            maxlength="200"
            :class="this.firstNameValidation.nameClasses"
            @blur="() => validateFirstName(this.firstName)">
          </o-input>
        </o-field>
      </div>
      <div class="field">
        <o-field class="label" label="* Last Name:">
          <o-input
            class="input"
            v-model="lastName"
            maxlength="200"
            :class="this.lastNameValidation.nameClasses"
            @blur="() => validateLastName(this.lastName)">
          </o-input>
        </o-field>
      </div>
      <div class="field">
        <o-field class="label" label="* Work Email Address:">
          <o-input
            class="input"
            v-model="workEmail"
            :class="this.workEmailValidation.emailClasses"
            @blur="() => validateWorkEmail(this.workEmail)">
          </o-input>
        </o-field>
      </div>
      <div v-if="role === 'DataCustodians'" class="field">
        <p class="has-text-weight-bold pb-2">Please confirm:</p>
        <p class="pb-2">{{ registerReference }}</p>
        <o-checkbox v-model="referenceCheckbox"> Yes </o-checkbox>
      </div>
      <div v-if="role === 'DataCustodians'" class="field">
        <p class="pb-2">{{ registerPolicy }}</p>
        <o-checkbox v-model="policyCheckbox"> Yes </o-checkbox>
      </div>
      <o-field label="Select your organisation:">
        <o-autocomplete
          v-if="organisationOptions"
          v-model="organisations"
          expanded
          placeholder="e.g. CSIRO"
          clearable
          :data="filteredOrganisationsObj"
          field="name"
          @select="(option) => this.selectOrg(option)">
          <template #empty>No results found</template>
        </o-autocomplete>
      </o-field>
      <div class="pt-6 is-flex is-justify-content-center">
        <p class="has-text-weight-bold is-size-5">OR</p>
      </div>
      <div class="field pt-6">
        <p class="has-text-weight-bold">Organisation not listed? Enter organisation ABN to find your organisation</p>
        <o-input
          class="input"
          :class="lookupABNValidation.abnClasses"
          @blur="validateABN(this.lookupABN)"
          v-model="lookupABN">
        </o-input>
        <o-button class="pt-2" @click="abnLookup">Search ABN</o-button>
      </div>
      <div class="field">
        <o-field label="Organisation Name">
          <o-input class="input" v-model="organisationName" disabled> </o-input>
        </o-field>
      </div>
      <div class="field">
        <o-field label="Organisation ABN">
          <o-input class="input" v-model="organisationABN" disabled> </o-input>
        </o-field>
      </div>
      <div class="field">
        <o-field label="* Organisation email address for notifications (different to your work email address)">
          <o-input
            class="input"
            :class="organisationEmailValidation.emailClasses"
            v-model="organisationEmail"
            :disabled="orgSelected"
            @blur="validateOrganisationEmail(this.organisationEmail)">
          </o-input>
        </o-field>
      </div>
      <div class="field is-flex">
        <o-checkbox v-model="termsCheckbox"></o-checkbox>
        <p>{{ registerTerms }}</p>
      </div>
      <div class="field is-grouped buttons is-pulled-right">
        <o-button
          variant="primary"
          type="button"
          :class="{ 'is-loading': this.loading }"
          :disabled="!canSubmitForm || this.loading"
          @click="this.registerUser"
          >Register</o-button
        >
      </div>
      <div v-if="duplicateOrgWarning" class="notification is-warning mt-4">
        <button class="delete" @click="duplicateOrgWarning = ''"></button>
        {{ duplicateOrgWarning }}
      </div>
    </div>
  </div>
</template>

<script>
import { getOrganisationsAPI, lookupABNAPI, registerAPI } from '../api/api';
import { useProgrammatic } from '@oruga-ui/oruga-next';
import { abnValidator, emailValidator, nameValidator } from '@/helpers/helpers';
import PageHeadingWithDescription from '@/components/PageHeadingWithDescription.vue';
import isEmail from 'validator/es/lib/isEmail';

export default {
  name: 'DataCustodianRegisterView',
  components: { PageHeadingWithDescription },
  props: {
    role: String,
  },
  beforeMount() {
    this.getOptions();
  },
  data() {
    return {
      firstName: '',
      firstNameValidation: {
        nameClasses: '',
        nameMessage: '',
      },
      lastName: '',
      lastNameValidation: {
        nameClasses: '',
        nameMessage: '',
      },
      workEmail: '',
      workEmailValidation: {
        emailClasses: '',
        emailMessage: '',
      },
      checkbox: false,
      organisations: '',
      organisationLookup: null,
      organisationOptions: [],
      selectedOrg: null,
      abn: '',
      lookupABN: '',
      lookupABNValidation: {
        abnClasses: '',
        abnMessage: '',
      },
      organisationName: '',
      organisationABN: '',
      organisationEmail: '',
      organisationEmailValidation: {
        emailClasses: '',
        emailMessage: '',
      },
      filteredOrganisationsObj: [],
      referenceCheckbox: false,
      policyCheckbox: false,
      termsCheckbox: false,
      orgSelected: false,
      registerReference: '* You can refer to a public website showing you are a legitimate custodian.',
      registerPolicy:
        '* Your organisation has a publicly accessible RASD policy that is compliant with the RASD framework.',
      registerTerms:
        '* When registering as a Data Custodian or Data Requestor with the RASDS, you agree to adhere to these Terms of Use. Any personal information that you provide will be used for the purpose of establishing your account with and facilitating data access via the RASDS, and will be handled in accordance with the RASDS Privacy Notice.',
      loading: false,
      duplicateOrgWarning: '', // Add warning message for duplicate organization
      existingOrgSuggestion: null, // Store existing org when duplicate is detected
    };
  },
  computed: {
    filteredOrganisations() {
      return this.organisationOptions.filter(
        (option) => option.name.toLowerCase().indexOf(this.organisations.toLowerCase()) >= 0
      );
    },

    canSubmitForm() {
      return (
        this.firstNameValidation.valid &&
        this.lastNameValidation.valid &&
        this.workEmailValidation.valid &&
        this.organisationName !== '' &&
        this.organisationABN !== '' &&
        this.orgEmailValid &&
        this.agreementsFilled
      );
    },
    subtitle() {
      return this.role === 'DataCustodians' ? 'Data Custodian Registration' : 'Data Requestor Registration';
    },
    agreementsFilled() {
      if (this.role === 'DataCustodians') {
        return this.referenceCheckbox && this.policyCheckbox && this.termsCheckbox;
      } else {
        return this.termsCheckbox;
      }
    },
    orgEmailValid() {
      return isEmail(this.organisationEmail) && this.organisationEmail !== this.workEmail;
    },
  },
  watch: {
    filteredOrganisations(newFilteredOrganisationsObj) {
      this.filteredOrganisationsObj = newFilteredOrganisationsObj;
    },
    organisationLookup(newOrganisationLookup) {
      this.organisationName = newOrganisationLookup?.EntityName;
      this.organisationABN = newOrganisationLookup?.Abn;
      if (this.organisations.length > 0) {
        this.organisations = '';
      }
    },
    selectedOrg(newSelectedOrg) {
      if (newSelectedOrg !== null) {
        this.organisationName = newSelectedOrg?.name;
        this.organisationABN = newSelectedOrg?.abn;
        this.organisationEmail = newSelectedOrg?.email;
      }
      if (this.lookupABN !== '' && newSelectedOrg !== null) {
        this.lookupABN = '';
      }
    },

    // Watch for when users clear the organization selection
    organisations(newValue) {
      // If user clears the organization dropdown but manual fields are still filled
      if (!newValue && !this.selectedOrg && this.organisationName && this.organisationABN) {
        // Check if the manual details match an existing organization
        const existingOrg = this.checkForExistingOrganisation(this.organisationName, this.organisationABN);

        if (existingOrg) {
          // Auto-reselect the existing organization and show helpful message
          this.handleExistingOrganisation(existingOrg);
        }
      }
    },
  },
  methods: {
    async getOptions() {
      this.organisationOptions = await getOrganisationsAPI();
    },
    async abnLookup() {
      const { oruga } = useProgrammatic();
      this.organisationEmail = '';
      this.orgSelected = false;
      this.duplicateOrgWarning = ''; // Clear any previous warnings

      this.organisationLookup = await lookupABNAPI(this.lookupABN);

      if (this.organisationLookup?.AbnStatus === 'Active') {
        // Check if this organization already exists in RASD
        const existingOrg = this.checkForExistingOrganisation(
          this.organisationLookup.EntityName,
          this.organisationLookup.Abn
        );

        if (existingOrg) {
          // Organization already exists - auto-select it and show helpful message
          this.handleExistingOrganisation(existingOrg);
        } else {
          oruga.notification.open({
            message: 'Organisation Added!',
            position: 'top',
            closable: true,
            variant: 'success',
            duration: 10000,
          });
        }
      } else {
        oruga.notification.open({
          message: 'Search text is not a valid ABN or ACN',
          position: 'top',
          closable: true,
          variant: 'danger',
          duration: 10000,
        });
      }
    },
    selectOrg(option) {
      this.selectedOrg = option;
      if (!this.organisationLookup) {
        this.orgSelected = true;
      }
      // Clear any duplicate warnings when user selects from dropdown
      this.duplicateOrgWarning = '';
    },
    async registerUser() {
      const { oruga } = useProgrammatic();

      // If no organization is selected but manual details are filled, check for duplicates
      if (!this.selectedOrg && this.organisationName && this.organisationABN) {
        const existingOrg = this.checkForExistingOrganisation(this.organisationName, this.organisationABN);

        if (existingOrg) {
          // Found existing organization - auto-select it and show helpful message
          this.handleExistingOrganisation(existingOrg);
          oruga.notification.open({
            message:
              'We found your organisation in our system and have selected it for you. Please click Register again to continue.',
            position: 'top',
            closable: true,
            variant: 'warning',
            duration: 10000,
          });
          return; // Exit early to let user confirm the auto-selection
        }
      }

      const org = this.selectedOrg?.id || {
        name: this.organisationName,
        abn: this.organisationABN,
        email: this.organisationEmail,
      };

      const agreements =
        this.role === 'DataCustodians'
          ? [this.registerReference, this.registerPolicy, this.registerTerms]
          : [this.registerTerms];

      this.loading = true;

      try {
        this.notification = await registerAPI(
          this.workEmail,
          this.firstName,
          this.lastName,
          this.role,
          org,
          agreements
        );
        this.loading = false;

        // Provide more specific error messages for organization-related issues
        let message = this.notification[0];
        if (!this.notification[1] && message.includes('already exists')) {
          message =
            'This organisation is already registered with RASD. Please select your organisation from the dropdown list above instead of entering it manually.';
        }

        oruga.notification.open({
          message: message,
          position: 'top',
          closable: true,
          variant: this.notification[1] ? 'success' : 'danger',
          duration: 10000,
        });

        if (this.notification[1]) {
          // Clear form and redirect on success
          this.firstName = '';
          this.lastName = '';
          this.workEmail = '';
          this.organisationName = '';
          this.organisationEmail = '';
          this.organisationABN = '';
          this.organisationLookup = '';
          this.referenceCheckbox = false;
          this.policyCheckbox = false;
          this.termsCheckbox = false;
          this.selectedOrg = null;
          this.lookupABN = '';
          this.duplicateOrgWarning = '';
          this.$router.push({ name: 'home' });
        }
      } catch (error) {
        this.loading = false;
        oruga.notification.open({
          message: 'There was an error processing your registration. Please try again or contact support.',
          position: 'top',
          closable: true,
          variant: 'danger',
          duration: 10000,
        });
      }
    },
    validateFirstName(name) {
      this.firstNameValidation = nameValidator(name);
    },
    validateLastName(name) {
      this.lastNameValidation = nameValidator(name);
    },
    validateABN(abn) {
      this.lookupABNValidation = abnValidator(abn);
    },
    validateWorkEmail(email) {
      this.workEmailValidation = emailValidator(email);
    },
    validateOrganisationEmail(email) {
      this.organisationEmailValidation = emailValidator(email);
    },

    // Check if an organization already exists in RASD by name or ABN
    checkForExistingOrganisation(entityName, abn) {
      // First check for exact ABN match
      let existingOrg = this.organisationOptions.find((org) => org.abn === abn);

      if (!existingOrg) {
        // If no ABN match, check for similar name matches
        const normalizedEntityName = entityName.toLowerCase().trim();
        existingOrg = this.organisationOptions.find((org) => org.name.toLowerCase().trim() === normalizedEntityName);
      }

      return existingOrg || null;
    },

    // Handle when an existing organization is detected
    handleExistingOrganisation(existingOrg) {
      const { oruga } = useProgrammatic();

      // Auto-select the existing organization
      this.selectedOrg = existingOrg;
      this.organisations = existingOrg.name;
      this.orgSelected = true;

      // Clear the manual ABN lookup fields
      this.lookupABN = '';
      this.organisationLookup = null;

      // Show helpful notification
      oruga.notification.open({
        message: `This organisation is already registered with RASD. We've automatically selected "${existingOrg.name}" for you.`,
        position: 'top',
        closable: true,
        variant: 'info',
        duration: 10000,
      });
    },
  },
};
</script>

<style scoped></style>
