<template>
  <div class="container">
    <div class="section">
      <div>
        <div class="is-flex is-justify-content-space-between mb-4">
          <h2 class="is-size-3">Data {{ group === UserGroup.DataCustodians ? 'Custodian' : 'Requestor' }} Request</h2>
          <button class="button is-primary" @click="this.$emit('back', true)">Back</button>
        </div>
        <div class="field">
          <o-field class="label">First name</o-field>
          <o-input :model-value="givenName" disabled />
        </div>
        <div class="field">
          <o-field class="label">Surname</o-field>
          <o-input :model-value="familyName" disabled />
        </div>
        <div class="field">
          <o-field class="label">Work email address</o-field>
          <o-input :model-value="username" disabled />
        </div>
        <div class="field">
          <o-field class="label">Organisation ABN</o-field>
          <o-input :model-value="organisationABN" disabled />
        </div>
        <div class="field">
          <o-field class="label">Organisation Name</o-field>
          <o-input :model-value="organisationName" disabled />
        </div>
        <div class="field">
          <o-field class="label">Organisation Email</o-field>
          <o-input :model-value="organisationEmail" disabled />
        </div>
        <div class="card mt-4 mb-6">
          <div class="card-content">
            <o-field class="label">Agreements</o-field>
            <o-checkbox v-for="agreement in agreements" :model-value="true" disabled>
              {{ agreement }}
            </o-checkbox>
          </div>
        </div>
        <o-checkbox
          :model-value="confirmed || status !== RegistrationStatus.NEW"
          :disabled="status !== RegistrationStatus.NEW"
          @change.stop="setConfirmed($event.target.checked)">
          <template v-if="organisationId"> I confirm that I have reviewed this request. </template>
          <template v-else>
            I confirm that I have reviewed this request.
            <b>This will create a new organisation.</b>
          </template>
        </o-checkbox>
        <div class="mt-4 mb-4 container is-flex is-justify-content-end">
          <!-- For users whose temporary password expired before they set their password -->
          <o-button
            v-if="status === RegistrationStatus.APPROVED"
            class="button mr-4"
            :class="{ 'is-loading': loading }"
            variant="primary"
            outlined
            @click="resendTemporaryPassword"
            :disabled="loading">
            Resend temporary password</o-button
          >
          <o-button
            class="button mr-4"
            :class="{ 'is-loading': this.loading }"
            variant="danger"
            @click="approveRequest(id, false)"
            :disabled="!confirmed || this.loading">
            Decline request</o-button
          >
          <o-button
            class="button"
            :class="{ 'is-loading': this.loading }"
            variant="primary"
            @click="approveRequest(id, true)"
            :disabled="!confirmed || this.loading">
            Approve request</o-button
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { approveRequestAPI, resendTemporaryPasswordAPI } from '@/api/api';
import { useProgrammatic } from '@oruga-ui/oruga-next';
import { RegistrationStatus, UserGroup } from '@/api/api.types';

export default defineComponent({
  name: 'RegistrationRequestsApproval',
  computed: {
    UserGroup() {
      return UserGroup;
    },
    RegistrationStatus() {
      return RegistrationStatus;
    },
  },
  props: {
    id: { type: String, default: undefined },
    givenName: { type: String, default: '' },
    familyName: { type: String, default: '' },
    username: { type: String, default: '' },
    organisationId: { type: String, default: undefined },
    organisationABN: { type: String, default: '' },
    organisationName: { type: String, default: '' },
    organisationEmail: { type: String, default: '' },
    agreements: { type: Array, default: () => [] },
    group: { type: String },
    status: { type: String },
  },
  data() {
    return {
      confirmed: false,
      loading: false,
    };
  },
  methods: {
    setConfirmed(checked: boolean) {
      this.confirmed = checked;
    },
    async approveRequest(id: string, approve: boolean) {
      this.loading = true;
      const response = await approveRequestAPI(id, approve);
      this.loading = false;
      const { oruga } = useProgrammatic();
      const message = response.error
        ? response.error.message
        : `Request for ${this.givenName} ${this.familyName} was successfully ${approve ? 'approved' : 'declined'}.`;
      oruga.notification.open({
        message: message,
        position: 'top',
        closable: true,
        variant: response.error ? 'danger' : 'success',
        duration: 10000,
      });
      if (!response.error) {
        this.$emit('back', true);
      }
    },
    async resendTemporaryPassword() {
      if (
        !this.id ||
        !confirm(
          `Send a new temporary password to ${this.givenName} ${this.familyName} (${this.username})? This only works if they have not yet set their password.`
        )
      ) {
        return;
      }
      this.loading = true;
      const response = await resendTemporaryPasswordAPI(this.id);
      this.loading = false;
      const { oruga } = useProgrammatic();
      const message = response.error
        ? response.error.message
        : `A new temporary password was sent to ${this.username}.`;
      oruga.notification.open({
        message: message,
        position: 'top',
        closable: true,
        variant: response.error ? 'danger' : 'success',
        duration: 10000,
      });
    },
  },
});
</script>
