<template>
  <div class="container">
    <div class="section">
      <div>
        <div v-if="!readOnlyFields" class="is-flex is-justify-content-end mb-4">
          <button class="button" @click="$emit('back', true)">Back</button>
        </div>
        <h1 class="subtitle is-2 has-text-centered mb-6">Restricted Access Species Data Access Request Form</h1>
        <div class="mb-4">
          <div class="field">
            <h2 class="is-size-3">Organisation/research institution name</h2>
            <o-input v-model="organisationName" disabled />
          </div>
          <validated-field
            v-model:value="organisationAddress"
            v-model:is-dirty="dirtyFields.organisationAddress"
            label="* Address"
            :message="validationErrors.organisationAddress"
            :disabled="!!readOnlyFields" />
          <validated-field
            type="checkbox-boolean"
            v-model:value="isIndigenousOrg"
            v-model:is-dirty="dirtyFields.isIndigenousOrg"
            label="* Indigenous body/organisation?"
            :message="validationErrors.isIndigenousOrg"
            :disabled="!!readOnlyFields" />
        </div>
        <div>
          <div>
            <h2 class="is-size-3 mt-6">Requestor</h2>
            <small>Must be an accountable representative of the organisation</small>
          </div>
        </div>
        <div class="field">
          <o-field label="* First name">
            <o-input v-model="givenName" disabled />
          </o-field>
        </div>
        <div class="field">
          <o-field label="* Last name">
            <o-input v-model="familyName" disabled />
          </o-field>
        </div>
        <div class="field">
          <o-field label="* Work email address">
            <o-input v-model="email" disabled />
          </o-field>
        </div>
        <validated-field
          v-model:value="orcId"
          v-model:is-dirty="dirtyFields.orcId"
          type="input"
          label="OrcID"
          :disabled="!!readOnlyFields"
          placeholder="e.g. 1111-1111-1111-1111" />
        <h2 class="is-size-3 mt-6">Project</h2>
        <validated-field
          v-model:value="projectTitle"
          v-model:is-dirty="dirtyFields.projectTitle"
          type="input"
          label="* Project title"
          :message="validationErrors.projectTitle"
          :disabled="!!readOnlyFields" />
        <validated-field
          v-model:value="purpose"
          v-model:is-dirty="dirtyFields.purpose"
          type="select"
          label="* What is the purpose of the data request?"
          :options="purposeValues"
          :message="validationErrors.purpose"
          :disabled="!!readOnlyFields" />
        <validated-field
          v-model:value="researchTopic"
          v-model:is-dirty="dirtyFields.researchTopic"
          type="select"
          label="Topic of research"
          sub-label="If applicable"
          :options="researchClassificationValues"
          :message="validationErrors.researchTopic"
          :disabled="industryType || !!readOnlyFields">
        </validated-field>
        <small>OR</small>
        <validated-field
          v-model:value="industryType"
          v-model:is-dirty="dirtyFields.industryType"
          type="select"
          label="Industry type"
          :options="industryClassificationValues"
          :message="validationErrors.industryType"
          :disabled="researchTopic || !!readOnlyFields">
        </validated-field>
        <validated-field
          v-model:value="commercialPurposes"
          v-model:is-dirty="dirtyFields.commercialPurposes"
          type="checkbox-boolean"
          label="* Is the data to be used for commercial purposes?"
          :message="validationErrors.commercialPurposes"
          :disabled="!!readOnlyFields">
        </validated-field>
        <validated-field
          v-model:value="publicBenefit"
          v-model:is-dirty="dirtyFields.publicBenefit"
          type="textarea"
          label="* Public benefit statement"
          sub-label="Is there a public interest in the outputs and outcomes of this project?"
          :message="validationErrors.publicBenefit"
          :disabled="!!readOnlyFields">
        </validated-field>
        <validated-field
          v-model:value="dataRequested"
          v-model:is-dirty="dirtyFields.dataRequested"
          type="textarea"
          label="* Data requested"
          sub-label="Provide details of the data you need e.g. taxa / species, area of interest etc"
          :message="validationErrors.dataRequested"
          :disabled="!!readOnlyFields" />
        <validated-field
          v-model:value="dataRelevance"
          v-model:is-dirty="dirtyFields.dataRelevance"
          type="textarea"
          label="* Relevance of data to project"
          :message="validationErrors.dataRelevance"
          :disabled="!!readOnlyFields" />
        <validated-field
          v-model:value="frequency"
          v-model:is-dirty="dirtyFields.frequency"
          type="shell"
          label="* How often do you require this data?"
          :message="validationErrors.frequency"
          :disabled="!!readOnlyFields">
          <o-checkbox
            :model-value="frequency === Frequency.Single"
            @change="setRequiredFrequency(Frequency.Single, $event.target.checked)"
            @blur="dirtyFields.frequency = true"
            :disabled="!!readOnlyFields">
            Single once off
          </o-checkbox>
          <o-checkbox
            :model-value="frequency === Frequency.Defined"
            @change="setRequiredFrequency(Frequency.Defined, $event.target.checked)"
            @blur="dirtyFields.frequency = true"
            :disabled="!!readOnlyFields">
            Defined period
          </o-checkbox>
          <o-checkbox
            :model-value="frequency === Frequency.Ongoing"
            @change="setRequiredFrequency(Frequency.Ongoing, $event.target.checked)"
            @blur="dirtyFields.frequency = true"
            :disabled="!!readOnlyFields">
            Ongoing
          </o-checkbox>
        </validated-field>
        <validated-field
          v-model:value="dateRequiredFrom"
          v-model:is-dirty="dirtyFields.dateRequiredFrom"
          type="datepicker"
          label="Date required from"
          :message="validationErrors.dateRequiredFrom"
          :disabled="frequency !== Frequency.Defined || !!readOnlyFields"
          include-reset
          @reset="resetFromDate">
        </validated-field>
        <validated-field
          v-model:value="dateRequiredTo"
          v-model:is-dirty="dirtyFields.dateRequiredTo"
          type="datepicker"
          label="Date required to"
          :message="validationErrors.dateRequiredTo"
          :disabled="frequency !== Frequency.Defined || !!readOnlyFields"
          include-reset
          @reset="resetToDate">
        </validated-field>
        <validated-field
          v-model:value="requiredPeriod"
          v-model:is-dirty="dirtyFields.requiredPeriod"
          type="textarea"
          label="What frequency and time period do you need the data for"
          sub-label="If ongoing, provide reasons to support this"
          :message="validationErrors.requiredPeriod"
          :disabled="frequency !== Frequency.Ongoing || !!readOnlyFields" />
        <validated-field
          v-model:value="requiredArea"
          v-model:is-dirty="dirtyFields.requiredArea"
          type="shell"
          label="* Area"
          :message="validationErrors.requiredArea"
          :disabled="!!readOnlyFields">
          <o-checkbox
            :model-value="requiredArea === Area.Whole"
            @change="setRequiredArea(Area.Whole, $event.target.checked)"
            @blur="dirtyFields.requiredArea = true"
            :disabled="!!readOnlyFields">
            Whole dataset
          </o-checkbox>
          <o-checkbox
            :model-value="requiredArea === Area.Specific"
            @change="setRequiredArea(Area.Specific, $event.target.checked)"
            @blur="dirtyFields.requiredArea = true"
            :disabled="!!readOnlyFields">
            Specific area
          </o-checkbox>
        </validated-field>
        <validated-field
          v-model:value="boundingBox"
          v-model:is-dirty="dirtyFields.boundingBox"
          type="textarea"
          sub-label="Provide bounding box - i.e. maximum and minimum latitudes and longitudes in decimal degrees using
            datum GDA94"
          :message="validationErrors.boundingBox"
          :disabled="requiredArea !== Area.Specific || !!readOnlyFields" />
        <validated-field
          v-model:value="securityControls"
          v-model:is-dirty="dirtyFields.securityControls"
          type="textarea"
          label="* What physical and IT controls will you use to ensure that the data is safe and secure during storage and use?"
          :message="validationErrors.securityControls"
          :disabled="!!readOnlyFields" />
        <validated-field
          v-model:value="userAccess"
          v-model:isDirty="dirtyFields.userAccess"
          type="select"
          label="* Who will be able to access the data?"
          :options="accessValues"
          :message="validationErrors.userAccess"
          :disabled="!!readOnlyFields" />
        <validated-field
          v-model:value="groupAccessName"
          v-model:is-dirty="dirtyFields.groupAccessName"
          type="textarea"
          label="* Name of the group of people accessing the data"
          sub-label="May be a business, organisational group, project team, etc."
          :message="validationErrors.groupAccessName"
          :disabled="!!readOnlyFields" />
        <validated-field
          v-model:value="distributedTo"
          v-model:is-dirty="dirtyFields.distributedTo"
          label="* Does your proposed use of the data involve distribution of projects (including publications) created from
            the data outside your organisation?"
          sub-label="Describe how and to whom these products will be distributed and/or presented, including any data transformations"
          type="textarea"
          :message="validationErrors.distributedTo"
          :disabled="!!readOnlyFields" />
        <div>
          <label class="has-text-weight-bold"
            >* If your access to full resolution data is not approved, would you like to receive a transformed dataset
            (i.e. with records obfuscated or withheld according to the principles of the framework)? For more
            information about the framework see the
            <a href="https://rasd.org.au/" class="is-underlined">Restricted Access Species Data Framework.</a></label
          >
          <validated-field
            class="py-4"
            v-model:value="willAcceptTransformed"
            v-model:is-dirty="dirtyFields.willAcceptTransformed"
            type="checkbox-boolean"
            :message="validationErrors.willAcceptTransformed"
            :disabled="!!readOnlyFields">
          </validated-field>
        </div>

        <div v-if="!readOnlyFields" class="mt-4 mb-4 container is-flex is-justify-content-end">
          <o-button class="button mr-4" variant="danger" @click="$emit('back', true)"> Cancel</o-button>
          <o-button
            class="button"
            :class="{ 'is-loading': this.isLoading }"
            :disabled="this.isLoading"
            variant="primary"
            @click="submitDataAccessRequest()">
            Submit</o-button
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue';
import {
  type ApiError,
  Area,
  type DataAccessRequestRead,
  type DataAccessRequestWrite,
  Frequency,
} from '@/api/api.types';
import { submitAccessRequestAPI } from '@/api/api';
import { useProgrammatic } from '@oruga-ui/oruga-next';
import { bothHaveValueValidator, hasValueValidator, xorHasValueValidator } from '@/helpers/helpers';
import ValidatedField from '@/components/ValidatedField.vue';
import { useUserDataStore, type UserData } from '@/store';

interface DataAccessRequestState extends DataAccessRequestWrite {
  organisationABN: string;
  organisationName: string;
  organisationEmail?: string;
  givenName?: string;
  familyName?: string;
  email?: string;
  dirtyFields: Partial<Record<keyof DataAccessRequestWrite, boolean>>;
}

export default defineComponent({
  name: 'DataAccessRequest',
  components: { ValidatedField },
  props: {
    active: { type: Object as PropType<string[]>, default: () => [] as string[] },
    metadataIds: { type: Object as PropType<string[]>, default: () => [] as string[] },
    title: { type: String, default: '' },
    abstract: { type: String, default: '' },
    keywords: { type: Object as PropType<string[]>, default: () => [] as string[] },
    locations: { type: Object as PropType<string[]>, default: () => [] as string[] },
    organisationId: { type: String, default: '' },
    custodian: { type: String, default: '' },
    titleLower: { type: String, default: '' },
    abstractLower: { type: String, default: '' },
    accessValues: { type: Object as PropType<string[]> },
    industryClassificationValues: { type: Object as PropType<string[]> },
    purposeValues: { type: Object as PropType<string[]> },
    researchClassificationValues: { type: Object as PropType<string[]> },
    readOnlyFields: { type: Object as PropType<DataAccessRequestRead>, required: false },
  },
  data(): Omit<DataAccessRequestState, 'metadataIds'> {
    let data = {
      organisationABN: '',
      organisationName: '',
      organisationEmail: undefined,
      organisationAddress: undefined,
      isIndigenousOrg: undefined,
      givenName: undefined,
      familyName: undefined,
      email: undefined,
      orcId: undefined,
      projectTitle: undefined,
      purpose: undefined,
      researchTopic: undefined,
      industryType: undefined,
      commercialPurposes: undefined,
      publicBenefit: undefined,
      dataRequested: undefined,
      dataRelevance: undefined,
      requiredPeriod: undefined,
      dateRequiredFrom: undefined,
      dateRequiredTo: undefined,
      frequency: undefined,
      requiredArea: undefined,
      boundingBox: undefined,
      securityControls: undefined,
      userAccess: undefined,
      groupAccessName: undefined,
      distributedTo: undefined,
      willAcceptTransformed: undefined,
      dirtyFields: {},
      isLoading: false,
    };
    if (this.readOnlyFields) {
      data = {
        ...data,
        organisationABN: '',
        organisationName: this.readOnlyFields.requestor.organisationName,
        organisationEmail: this.readOnlyFields.requestor.organisationEmail,
        organisationAddress: this.readOnlyFields.requestor.organisationAddress,
        isIndigenousOrg: this.readOnlyFields.requestor.organisationIndigenousBody,
        givenName: this.readOnlyFields.requestor.givenName,
        familyName: this.readOnlyFields.requestor.familyName,
        email: this.readOnlyFields.requestor.email,
        orcId: this.readOnlyFields.requestor.orcid,
        projectTitle: this.readOnlyFields.project.title,
        purpose: this.readOnlyFields.project.purpose,
        researchTopic: this.readOnlyFields.project.research,
        industryType: this.readOnlyFields.project.industry,
        commercialPurposes: this.readOnlyFields.project.commercial,
        publicBenefit: this.readOnlyFields.project.publicBenefitExplanation,
        dataRequested: this.readOnlyFields.data.requested,
        dataRelevance: this.readOnlyFields.data.relevanceExplanation,
        requiredPeriod: this.readOnlyFields.data.frequencyExplanation,
        dateRequiredFrom:
          this.readOnlyFields.data.requiredFrom === null ? null : new Date(this.readOnlyFields.data.requiredFrom),
        dateRequiredTo:
          this.readOnlyFields.data.requiredTo === null ? null : new Date(this.readOnlyFields.data.requiredTo),
        frequency: this.readOnlyFields.data.frequency,
        requiredArea: this.readOnlyFields.data.area,
        boundingBox: this.readOnlyFields.data.areaExplanation,
        securityControls: this.readOnlyFields.data.securityExplanation,
        userAccess: this.readOnlyFields.data.access,
        groupAccessName: this.readOnlyFields.data.accessExplanation,
        distributedTo: this.readOnlyFields.data.distributionExplanation,
        willAcceptTransformed: this.readOnlyFields.data.acceptTransformed,
        isLoading: false,
      };
    }
    return data;
  },
  watch: {
    frequency: {
      handler: function (value) {
        if (value === Frequency.Single || value === Frequency.Ongoing) {
          this.resetSelectedDates();
        }
        if (value !== Frequency.Ongoing) {
          this.resetRequiredPeriod();
        }
      },
      immediate: true,
    },
    requiredArea: {
      handler: function (value) {
        if (value === Area.Whole) {
          this.resetBoundingBox();
        }
      },
      immediate: true,
    },
  },
  computed: {
    Frequency: () => Frequency,
    Area: () => Area,
    validationErrors() {
      return {
        organisationAddress: hasValueValidator(this.organisationAddress),
        isIndigenousOrg: hasValueValidator(this.isIndigenousOrg),
        projectTitle: hasValueValidator(this.projectTitle),
        purpose: hasValueValidator(this.purpose),
        researchTopic: xorHasValueValidator(this.researchTopic, {
          xorField: 'Industry type',
          xorValue: this.industryType,
        }),
        industryType: xorHasValueValidator(this.industryType, {
          xorField: 'Research topic',
          xorValue: this.researchTopic,
        }),
        commercialPurposes: hasValueValidator(this.commercialPurposes),
        publicBenefit: hasValueValidator(this.publicBenefit),
        dataRequested: hasValueValidator(this.dataRequested),
        dataRelevance: hasValueValidator(this.dataRelevance),
        frequency: hasValueValidator(this.frequency),
        dateRequiredFrom:
          this.frequency !== Frequency.Defined
            ? undefined
            : bothHaveValueValidator(this.dateRequiredFrom?.toLocaleDateString(), {
                andField: 'Date required to',
                andValue: this.dateRequiredTo?.toLocaleDateString(),
              }),
        dateRequiredTo:
          this.frequency !== Frequency.Defined
            ? undefined
            : bothHaveValueValidator(this.dateRequiredTo?.toLocaleDateString(), {
                andField: 'Date required from',
                andValue: this.dateRequiredFrom?.toLocaleDateString(),
              }),
        requiredPeriod: this.frequency === Frequency.Ongoing ? hasValueValidator(this.requiredPeriod) : undefined,
        requiredArea: hasValueValidator(this.requiredArea),
        boundingBox:
          this.requiredArea === Area.Whole
            ? undefined
            : bothHaveValueValidator(this.boundingBox, {
                andField: 'Area',
                andValue: this.requiredArea,
                xnor: true,
              }),
        securityControls: hasValueValidator(this.securityControls),
        userAccess: hasValueValidator(this.userAccess),
        groupAccessName: hasValueValidator(this.groupAccessName),
        distributedTo: hasValueValidator(this.distributedTo),
        willAcceptTransformed: hasValueValidator(this.willAcceptTransformed),
      };
    },
    validationErrorCount() {
      return Object.entries(this.validationErrors).filter(([, value]) => typeof value !== 'undefined');
    },
  },
  beforeMount() {
    const userDataStore: UserData = useUserDataStore();
    const sessionUserData = userDataStore || '{}';
    if (!this.readOnlyFields) {
      this.organisationABN = sessionUserData.organisationABN || '';
      this.organisationName = sessionUserData.organisationName || '';
      this.organisationEmail = sessionUserData.organisationEmail || '';
      this.givenName = sessionUserData?.givenName;
      this.familyName = sessionUserData?.familyName;
      this.email = sessionUserData?.email;
    }
    this.$router.push('');
  },
  methods: {
    setRequiredArea(area: Area, checked: boolean) {
      this.requiredArea = checked ? area : undefined;
    },
    setRequiredFrequency(frequency: Frequency, checked: boolean) {
      this.frequency = checked ? frequency : undefined;
      this.dirtyFields.frequency = true;
    },
    setWillAcceptTransformed(willAccept: boolean, checked: boolean) {
      this.willAcceptTransformed = checked ? willAccept : undefined;
    },
    resetSelectedDates() {
      this.dateRequiredFrom = undefined;
      this.dateRequiredTo = undefined;
    },
    resetFromDate() {
      this.dateRequiredFrom = undefined;
    },
    resetToDate() {
      this.dateRequiredTo = undefined;
    },
    resetRequiredPeriod() {
      this.requiredPeriod = undefined;
    },
    resetBoundingBox() {
      this.boundingBox = undefined;
    },
    async submitDataAccessRequest() {
      const { oruga } = useProgrammatic();
      let message: string | undefined;
      let error: ApiError | undefined;
      let notificationClass: string = 'success';
      if (this.validationErrorCount.length === 0) {
        this.isLoading = true;
        const response = await submitAccessRequestAPI({
          metadataIds: this.metadataIds,
          organisationAddress: this.organisationAddress,
          isIndigenousOrg: this.isIndigenousOrg,
          orcId: this.orcId,
          projectTitle: this.projectTitle,
          purpose: this.purpose,
          researchTopic: this.researchTopic,
          industryType: this.industryType,
          commercialPurposes: this.commercialPurposes,
          publicBenefit: this.publicBenefit,
          dataRequested: this.dataRequested,
          dataRelevance: this.dataRelevance,
          requiredPeriod: this.requiredPeriod,
          dateRequiredFrom: this.dateRequiredFrom,
          dateRequiredTo: this.dateRequiredTo,
          frequency: this.frequency,
          requiredArea: this.requiredArea,
          boundingBox: this.boundingBox,
          securityControls: this.securityControls,
          userAccess: this.userAccess,
          groupAccessName: this.groupAccessName,
          distributedTo: this.distributedTo,
          willAcceptTransformed: this.willAcceptTransformed,
        });
        this.isLoading = false;
        error = response.error;
        if (error) {
          message = error.detail
            ? (message = `${error.detail.map((detail) => detail.msg).join('<br>')}`)
            : error.message;
          notificationClass = 'danger';
        } else {
          this.$emit('back', true);
          message = `${response.data?.id} - Your request has been successfully submitted. The Data Custodian will contact you`;
        }
      } else {
        for (const validationError in this.validationErrors) {
          this.dirtyFields[validationError as keyof DataAccessRequestWrite] = true;
        }
        message = `There are <b>${this.validationErrorCount.length}</b> errors on the form.`;
        notificationClass = 'danger';
      }
      this.isLoading = false;
      oruga.notification.open({
        message: message,
        position: 'top',
        closable: true,
        variant: notificationClass,
        duration: 10000,
      });
    },
  },
});
</script>
