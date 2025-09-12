<template>
  <PageHeading pageTitle="Metadata / Edit" />
  <div class="container">
    <div v-if="metadata" class="section">
      <div class="level">
        <div class="level-left">
          <router-link to="/metadata">Go Back</router-link>
        </div>
        <div class="level-right">
          <o-button v-if="!this.editMode" class="button mr-4 is-align-items-self-end" @click="this.setEditMode()"
            >Edit</o-button
          >
          <o-button v-if="!this.editMode" class="button is-danger is-align-items-self-end" @click="this.confirmDelete()"
            >Delete</o-button
          >
        </div>
      </div>
      <h2 class="is-size-3">Metadata details</h2>
      <div class="field">
        <o-field
          class="label"
          :variant="this.titleValidation.titleClasses === 'is-danger' ? 'danger' : ''"
          :message="this.titleValidation.titleClasses === 'is-danger' ? 'Title must not be empty' : ''"
          >* Title:</o-field
        >
        <o-input
          v-model="metadata.title"
          :disabled="!editMode"
          :class="this.titleValidation.titleClasses"
          maxlength="200"
          @blur="this.titleValidate"></o-input>
      </div>
      <div class="field">
        <o-field
          class="label"
          :variant="this.abstractValidation.abstractClasses === 'is-danger' ? 'danger' : ''"
          :message="this.abstractValidation.abstractClasses === 'is-danger' ? 'Abstract must not be empty' : ''"
          >* Abstract:</o-field
        >
        <o-input
          v-model="metadata.abstract"
          :class="this.abstractValidation.abstractClasses"
          maxlength="2000"
          type="textarea"
          rows="4"
          :disabled="!editMode"
          @blur="this.abstractValidate"></o-input>
        <p class="help" :class="{ 'has-text-danger': metadata.abstract && metadata.abstract.length >= 2000 }">
          {{ metadata.abstract ? metadata.abstract.length : 0 }}/2000 characters
          <span v-if="metadata.abstract && metadata.abstract.length >= 2000" class="has-text-danger"
            >- Limit reached!</span
          >
        </p>
      </div>
      <div class="field">
        <o-field
          class="label"
          :variant="this.keywordValidation.keywordClasses === 'is-danger' ? 'danger' : ''"
          :message="this.keywordValidation.keywordClasses === 'is-danger' ? 'Keywords must not be empty' : ''"
          >* Keywords:</o-field
        >
        <o-dropdown
          v-if="keywordsOptions"
          :disabled="!editMode"
          v-model="metadata.keywords"
          @change="this.keywordValidate"
          multiple
          role="list">
          <template #trigger>
            <o-button variant="primary" type="button" :class="this.keywordValidation.keywordClasses">
              <span v-if="metadata.keywords"
                >{{ keywords_text }}
                <span v-if="metadata.keywords.length > 8">...</span>
              </span>
            </o-button>
          </template>
          <o-dropdown-item v-for="keyword in keywordsOptions" :value="keyword">{{ keyword }}</o-dropdown-item>
        </o-dropdown>
      </div>
      <div class="field">
        <o-field
          class="label"
          :variant="this.temporalCoverageFromValidation.temporalCoverageFromClasses === 'is-danger' ? 'danger' : ''"
          :message="
            this.temporalCoverageFromValidation.temporalCoverageFromClasses === 'is-danger'
              ? 'Temporal Coverage From must not be empty'
              : ''
          "
          >* Temporal Coverage From:</o-field
        >
        <o-datepicker
          v-model="metadata.temporal_coverage_from"
          :disabled="!editMode"
          :class="this.temporalCoverageFromValidation.temporalCoverageFromClasses"
          @blur="this.temporalCoverageFromValidate"
          :min-date="minDate">
        </o-datepicker>
      </div>
      <div class="field">
        <o-field
          class="label"
          :variant="this.temporalCoverageToValidation.temporalCoverageToClasses === 'is-danger' ? 'danger' : ''"
          :message="
            this.temporalCoverageToValidation.temporalCoverageToClasses === 'is-danger'
              ? 'Temporal Coverage To must not be empty'
              : ''
          "
          >* Temporal Coverage To:</o-field
        >
        <o-datepicker
          v-model="metadata.temporal_coverage_to"
          :disabled="!editMode"
          :class="this.temporalCoverageToValidation.temporalCoverageToClasses"
          @blur="this.temporalCoverageToValidate"
          :min-date="minDate"></o-datepicker>
      </div>
      <div class="field">
        <o-field class="label" :message="editMode ? 'Please enter your value as an integer' : null"
          >* North Bounding Coordinate:</o-field
        >
        <o-input
          v-model="metadata.north_bounding_coordinate"
          :disabled="!editMode"
          :class="this.northBoundingCoordinateValidation.northBoundingCoordinateClasses"
          @blur="this.northBoundingCoordinateValidate"
          placeholder="e.g. 90"></o-input>
      </div>
      <div class="field">
        <o-field class="label" :message="editMode ? 'Please enter your value as an integer' : null"
          >* South Bounding Coordinate:</o-field
        >
        <o-input
          v-model="metadata.south_bounding_coordinate"
          :disabled="!editMode"
          :class="this.southBoundingCoordinateValidation.southBoundingCoordinateClasses"
          @blur="this.southBoundingCoordinateValidate"
          placeholder="e.g. 90"></o-input>
      </div>
      <div class="field">
        <o-field class="label" :message="editMode ? 'Please enter your value as an integer' : null"
          >* East Bounding Coordinate:</o-field
        >
        <o-input
          v-model="metadata.east_bounding_coordinate"
          :disabled="!editMode"
          :class="this.eastBoundingCoordinateValidation.eastBoundingCoordinateClasses"
          @blur="this.eastBoundingCoordinateValidate"
          placeholder="e.g. 180"></o-input>
      </div>
      <div class="field">
        <o-field class="label" :message="editMode ? 'Please enter your value as an integer' : null"
          >* West Bounding Coordinate:</o-field
        >
        <o-input
          v-model="metadata.west_bounding_coordinate"
          :disabled="!editMode"
          :class="this.westBoundingCoordinateValidation.westBoundingCoordinateClasses"
          @blur="this.westBoundingCoordinateValidate"
          placeholder="e.g. 180"></o-input>
      </div>
      <div class="field">
        <o-field
          class="label"
          :variant="this.locationsValidation.locationsClasses === 'is-danger' ? 'danger' : ''"
          :message="this.locationsValidation.locationsClasses === 'is-danger' ? 'Location must not be empty' : ''"
          >* Locations:</o-field
        >
        <o-dropdown
          v-model="metadata.locations"
          role="list"
          multiple
          @change="this.locationsValidate"
          :disabled="!editMode">
          <template #trigger>
            <o-button variant="primary" :class="this.locationsValidation.locationsClasses">
              {{ locations_text }}
              <span v-if="metadata.locations.length > 5">...</span>
            </o-button>
          </template>
          <o-dropdown-item v-for="location in locationsOptions" :value="location">{{ location }}</o-dropdown-item>
        </o-dropdown>
      </div>
      <div class="field">
        <o-field
          class="label"
          :variant="this.taxaCoveredValidation.taxaCoveredClasses === 'is-danger' ? 'danger' : ''"
          :message="
            this.taxaCoveredValidation.taxaCoveredClasses === 'is-danger' ? 'Taxa Covered must not be empty' : ''
          "
          >* Taxa Covered:</o-field
        >
        <o-input
          v-model="metadata.taxa_covered"
          :disabled="!editMode"
          :class="taxaCoveredValidation.taxaCoveredClasses"
          @blur="this.taxaCoveredValidate"
          maxlength="200"></o-input>
      </div>
      <div class="field">
        <o-field
          class="label"
          :variant="this.collectionMethodsValidation.collectionMethodsClasses === 'is-danger' ? 'danger' : ''"
          :message="
            this.collectionMethodsValidation.collectionMethodsClasses === 'is-danger'
              ? 'Collection Methods must not be empty'
              : ''
          "
          >* Collection Methods:</o-field
        >
        <o-dropdown
          v-model="metadata.collection_methods"
          @change="this.collectionMethodValidate"
          multiple
          role="list"
          :disabled="!editMode">
          <template #trigger>
            <o-button
              variant="primary"
              type="button"
              :class="this.collectionMethodsValidation.collectionMethodsClasses">
              <span>{{ collection_methods_text }}</span>
            </o-button>
          </template>
          <o-dropdown-item v-for="collection_method in collectionMethodsOptions" :value="collection_method">{{
            collection_method
          }}</o-dropdown-item>
        </o-dropdown>
      </div>
      <div class="field">
        <p class="pt-2 label">You must add at least the Data Source DOI or the Data Source URL</p>
        <o-field
          class="label"
          :variant="this.dataSourceValidation.dataSourceDOIClasses === 'is-danger' ? 'danger' : ''"
          :message="
            this.dataSourceValidation.dataSourceDOIClasses === 'is-danger'
              ? 'Data Source DOI must not be empty or DOI format is invalid'
              : ''
          "
          >Data Source DOI:</o-field
        >
        <o-input
          v-model="metadata.data_source_doi"
          :class="this.dataSourceValidation.dataSourceDOIClasses"
          @blur="this.dataSourceValidate"
          :disabled="!editMode"></o-input>
      </div>
      <div class="field">
        <o-field
          class="label"
          :variant="this.dataSourceValidation.dataSourceURLClasses === 'is-danger' ? 'danger' : ''"
          :message="
            this.dataSourceValidation.dataSourceURLClasses === 'is-danger'
              ? 'Data Source URL must not be empty or URL format is invalid'
              : ''
          "
          >Data Source URL:</o-field
        >
        <o-input
          v-model="metadata.data_source_url"
          :class="this.dataSourceValidation.dataSourceURLClasses"
          @blur="this.dataSourceValidate"
          :disabled="!editMode"></o-input>
      </div>
      <div class="field">
        <o-field class="label">* Embargoed:</o-field>
        <o-select
          @click="this.metadata.embargo_release_date = ''"
          v-model="this.metadata.embargoed"
          :disabled="!editMode">
          <option value="true">True</option>
          <option value="false">False</option>
        </o-select>
      </div>
      <div v-if="this.metadata.embargoed === 'true' || this.metadata.embargoed === true" class="field">
        <o-field class="label">Embargo Release Date: (Optional)</o-field>
        <o-datepicker v-model="this.metadata.embargo_release_date" :disabled="!editMode"></o-datepicker>
        <o-button class="mt-2" :disabled="!editMode" @click="this.metadata.embargo_release_date = ''"
          >Clear Date</o-button
        >
      </div>
      <div class="field">
        <o-field class="label">* Custodian:</o-field>
        <o-input
          v-model="metadata.custodian"
          :class="this.custodianValidation.custodianClasses"
          @blur="this.custodianValidate"
          :disabled="!editMode"
          maxlength="200"></o-input>
      </div>
      <div class="field">
        <o-field
          class="label"
          :variant="this.contactOrganisationValidation.contactOrganisationClasses === 'is-danger' ? 'danger' : ''"
          :message="
            this.contactOrganisationValidation.contactOrganisationClasses === 'is-danger'
              ? 'Contact Organisation must not be empty'
              : ''
          "
          >* Contact Organisation:</o-field
        >
        <o-input
          v-model="metadata.contact_organisation"
          :disabled="!editMode"
          :class="this.contactOrganisationValidation.contactOrganisationClasses"
          @blur="this.contactOrganisationValidate"
          maxlength="200"></o-input>
      </div>
      <div class="field">
        <o-field
          class="label"
          :variant="this.contactPositionValidation.contactPositionClasses === 'is-danger' ? 'danger' : ''"
          :message="
            this.contactPositionValidation.contactPositionClasses === 'is-danger'
              ? 'Contact Position must not be empty'
              : ''
          "
          >* Contact Position:</o-field
        >
        <o-input
          v-model="metadata.contact_position"
          :disabled="!editMode"
          :class="this.contactPositionValidation.contactPositionClasses"
          @blur="this.contactPositionValidate"
          maxlength="200"></o-input>
      </div>
      <div class="field">
        <o-field
          class="label"
          :variant="this.contactEmailValidation.emailClasses === 'is-danger' ? 'danger' : ''"
          :message="this.contactEmailValidation.emailClasses === 'is-danger' ? 'Contact Email must not be empty' : ''"
          >* Contact Email:</o-field
        >
        <o-input
          v-model="metadata.contact_email"
          :disabled="!editMode"
          :class="this.contactEmailValidation.emailClasses"
          @blur="this.contactEmailValidate"
          maxlength="200"></o-input>
      </div>
      <div class="field">
        <o-field
          class="label"
          :variant="this.storedFormatValidation.storedFormatClasses === 'is-danger' ? 'danger' : ''"
          :message="
            this.storedFormatValidation.storedFormatClasses === 'is-danger' ? 'Stored Format must not be empty' : ''
          "
          >* Stored Format:</o-field
        >
        <o-dropdown v-model="metadata.stored_format" @change="this.storedFormatValidate" :disabled="!editMode">
          <template #trigger>
            <o-button variant="primary" type="button" :class="this.storedFormatValidation.storedFormatClasses">
              <span>{{ metadata.stored_format ? metadata.stored_format : 'Select a stored format' }}</span>
            </o-button>
          </template>
          <o-dropdown-item v-for="storedFormat in formatsOptions" :value="storedFormat">{{
            storedFormat
          }}</o-dropdown-item>
        </o-dropdown>
      </div>
      <div class="field">
        <o-field
          class="label"
          :variant="this.availableFormatsValidation.availableFormatsClasses === 'is-danger' ? 'danger' : ''"
          :message="
            this.availableFormatsValidation.availableFormatsClasses === 'is-danger'
              ? 'Available Formats must not be empty'
              : ''
          "
          >* Available Formats:</o-field
        >
        <o-dropdown
          v-model="metadata.available_formats"
          multiple
          role="list"
          :disabled="!editMode"
          @change="this.availableFormatsValidate">
          <template #trigger>
            <o-button variant="primary" type="button" :class="this.availableFormatsValidation.availableFormatsClasses">
              <span>
                {{ available_formats_text }}
              </span>
            </o-button>
          </template>
          <o-dropdown-item v-for="availableFormat in formatsOptions" :value="availableFormat">{{
            availableFormat
          }}</o-dropdown-item>
        </o-dropdown>
      </div>
      <div class="field">
        <o-field
          class="label"
          :variant="this.accessRightsValidation.accessRightsClasses === 'is-danger' ? 'danger' : ''"
          :message="
            this.accessRightsValidation.accessRightsClasses === 'is-danger' ? 'Access Rights must not be empty' : ''
          "
          >* Access Rights:</o-field
        >
        <o-dropdown v-model="metadata.access_rights" :disabled="!editMode" @change="this.accessRightsValidate">
          <template #trigger>
            <o-button variant="primary" :class="this.accessRightsValidation.accessRightsClasses">
              <span>{{ metadata.access_rights ? metadata.access_rights : 'Please select an access right' }}</span>
            </o-button>
          </template>
          <o-dropdown-item v-for="accessRight in accessRightsOptions" :value="accessRight">{{
            accessRight
          }}</o-dropdown-item>
        </o-dropdown>
      </div>
      <div class="field">
        <o-field
          class="label"
          :variant="this.useRestrictionsValidation.useRestrictionsClasses === 'is-danger' ? 'danger' : ''"
          :message="
            this.useRestrictionsValidation.useRestrictionsClasses === 'is-danger'
              ? 'Use Restrictions must not be empty'
              : ''
          "
          >* Use Restrictions:</o-field
        >
        <o-input
          v-model="metadata.use_restrictions"
          :disabled="!editMode"
          :class="this.useRestrictionsValidation.useRestrictionsClasses"
          @blur="this.useRestrictionsValidate"
          maxlength="500"
          placeholder="Any specific use constraints on the dataset including legal, restricted access species, embargo periods etc in addition to access rights"></o-input>
      </div>
      <div class="field">
        <o-field
          class="label"
          :variant="this.securityClassificationValidation.securityClassificationClasses === 'is-danger' ? 'danger' : ''"
          :message="
            this.securityClassificationValidation.securityClassificationClasses === 'is-danger'
              ? 'Security Classification must not be empty'
              : ''
          "
          >* Security Classification:</o-field
        >
        <o-dropdown
          v-model="metadata.security_classification"
          :disabled="!editMode"
          @change="this.securityClassificationValidate">
          <template #trigger>
            <o-button variant="primary" :class="this.securityClassificationValidation.securityClassificationClasses">
              <span>{{
                metadata.security_classification ? metadata.security_classification : 'Select a security classification'
              }}</span>
            </o-button>
          </template>
          <o-dropdown-item
            v-for="securityClassification in securityClassificationOptions"
            :value="securityClassification"
            >{{ securityClassification }}</o-dropdown-item
          >
        </o-dropdown>
      </div>
      <div class="field">
        <o-field
          class="label"
          :variant="this.generalisationsValidation.generalisationsClasses === 'is-danger' ? 'danger' : ''"
          :message="
            this.generalisationsValidation.generalisationsClasses === 'is-danger'
              ? 'Generalisations must not be empty'
              : ''
          "
          >* Generalisations:</o-field
        >
        <o-input
          v-model="metadata.generalisations"
          :class="this.generalisationsValidation.generalisationsClasses"
          @blur="this.generalisationsValidate"
          :disabled="!editMode"
          maxlength="500"
          placeholder="Any rulesets which have been applied at a dataset level to obfuscate or generalise either species attributes or location or remove/modify personal identifiable information"></o-input>
      </div>
      <div class="is-flex is-justify-content-start">
        <o-button v-if="!this.editMode" class="button mr-4" @click="this.setEditMode()">Edit</o-button>
        <o-button v-if="!this.editMode" class="button is-danger mr-4" @click="this.confirmDelete()">Delete</o-button>
        <o-button
          v-if="this.editMode"
          :disabled="canSubmitForm || this.loading"
          class="button is-success mr-4"
          :class="{ 'is-loading': this.loading }"
          @click="this.editMetadata()"
          >Save</o-button
        >
      </div>
    </div>
    <div v-else class="section">
      <o-loading />
    </div>
  </div>
</template>

<script>
import PageHeading from '../components/PageHeading.vue';
import {
  editMetadataAPI,
  getMetadataAPI,
  getAccessRightsAPI,
  getCollectionMethodsAPI,
  getFormatsAPI,
  getKeywordsAPI,
  getLocationsAPI,
  getSecurityClassificationsAPI,
  deleteMetadataAPI,
} from '../api/api';
import {
  accessRightsValidator,
  availableFormatsValidator,
  collectionValidator,
  contactOrgValidator,
  contactPositionValidator,
  custodianValidator,
  dataSourceValidator,
  eastCoordinateValidator,
  emailValidator,
  generalisationsValidator,
  keywordsValidator,
  locationsValidator,
  northCoordinateValidator,
  securityClassificationValidator,
  southCoordinateValidator,
  storedFormatValidator,
  taxaValidator,
  temporalCoverageFromValidator,
  temporalCoverageToValidator,
  titleValidator,
  useRestrictionsValidator,
  westCoordinateValidator,
  abstractValidator,
} from '../helpers/helpers';
import { useProgrammatic } from '@oruga-ui/oruga-next';
export default {
  name: 'MetadataView',
  components: {
    PageHeading,
  },
  beforeMount() {
    this.getMetadata();
    this.getOptions();
  },
  computed: {
    canSubmitForm() {
      return !(
        this.titleValidation.valid &&
        this.keywordValidation.valid &&
        this.temporalCoverageFromValidation.valid &&
        this.temporalCoverageToValidation.valid &&
        this.northBoundingCoordinateValidation.valid &&
        this.southBoundingCoordinateValidation.valid &&
        this.eastBoundingCoordinateValidation.valid &&
        this.westBoundingCoordinateValidation.valid &&
        this.locationsValidation.valid &&
        this.taxaCoveredValidation.valid &&
        this.collectionMethodsValidation.valid &&
        this.dataSourceValidation.valid &&
        this.custodianValidation.valid &&
        this.contactOrganisationValidation.valid &&
        this.contactPositionValidation.valid &&
        this.contactEmailValidation.valid &&
        this.storedFormatValidation.valid &&
        this.accessRightsValidation.valid &&
        this.useRestrictionsValidation.valid &&
        this.securityClassificationValidation.valid &&
        this.generalisationsValidation.valid
      );
    },
    available_formats_text() {
      if (this.metadata.available_formats?.length === 0) {
        return 'Select an available format';
      } else {
        return this.metadata?.available_formats.toString();
      }
    },
    keywords_text() {
      if (this.metadata.keywords?.length === 0) {
        return 'Select a keyword';
      } else {
        return this.metadata?.keywords.slice(0, 8).join(', ').toString();
      }
    },
    locations_text() {
      if (this.metadata.locations?.length === 0) {
        return 'Select a location';
      } else {
        return this.metadata?.locations.slice(0, 7).toString();
      }
    },
    collection_methods_text() {
      if (this.metadata.collection_methods?.length === 0) {
        return 'Select a collection method';
      } else {
        return this.metadata?.collection_methods.join(', ').toString();
      }
    },
  },
  data() {
    return {
      loading: false,
      metadata: null,
      editMode: false,
      titleValidation: {
        valid: true,
        titleClasses: '',
      },
      keywordValidation: {
        valid: true,
        keywordClasses: '',
      },
      temporalCoverageFromValidation: {
        valid: true,
        temporalCoverageFromClasses: '',
      },
      temporalCoverageToValidation: {
        valid: true,
        temporalCoverageToClasses: '',
      },
      northBoundingCoordinateValidation: {
        valid: true,
        northBoundingCoordinateClasses: '',
      },
      southBoundingCoordinateValidation: {
        valid: true,
        southBoundingCoordinateClasses: '',
      },
      eastBoundingCoordinateValidation: {
        valid: true,
        eastBoundingCoordinateClasses: '',
      },
      westBoundingCoordinateValidation: {
        valid: true,
        westBoundingCoordinateClasses: '',
      },
      locationsValidation: {
        valid: true,
        locationsClasses: '',
      },
      taxaCoveredValidation: {
        valid: true,
        taxaCoveredClasses: '',
      },
      collectionMethodsValidation: {
        valid: true,
        collectionMethodsClasses: '',
      },
      dataSourceValidation: {
        valid: true,
        dataSourceDOIValidation: {
          valid: true,
          dataSourceDOIClasses: '',
        },
        dataSourceURLValidation: {
          valid: true,
          dataSourceURLClasses: '',
        },
      },
      custodianValidation: {
        valid: true,
        custodianClasses: '',
      },
      contactOrganisationValidation: {
        valid: true,
        contactOrganisationClasses: '',
      },
      contactPositionValidation: {
        valid: true,
        contactPositionClasses: '',
      },
      contactEmailValidation: {
        valid: true,
        contactEmailClasses: '',
      },
      storedFormatValidation: {
        valid: true,
        storedFormatClasses: '',
      },
      availableFormatsValidation: {
        valid: true,
        availableFormatsClasses: '',
      },
      accessRightsValidation: {
        valid: true,
        accessRightsClasses: '',
      },
      useRestrictionsValidation: {
        valid: true,
        useRestrictionsClasses: '',
      },
      securityClassificationValidation: {
        valid: true,
        securityClassificationClasses: '',
      },
      generalisationsValidation: {
        valid: true,
        generalisationsClasses: '',
      },
      abstractValidation: {
        valid: true,
        abstractClasses: '',
      },
      accessRightsOptions: [],
      collectionMethodsOptions: [],
      formatsOptions: [],
      keywordsOptions: [],
      locationsOptions: [],
      securityClassificationOptions: [],
      notification: null,
      minDate: new Date('1760-01-01'),
      submitting: false,
    };
  },
  watch: {
    metadata() {
      this.metadata.temporal_coverage_from = new Date(this.metadata.temporal_coverage_from);
      this.metadata.temporal_coverage_to = new Date(this.metadata.temporal_coverage_to);
      this.metadata.embargo_release_date =
        this.metadata.embargo_release_date === '1970-01-01' || this.metadata.embargo_release_date === null
          ? null
          : new Date(this.metadata.embargo_release_date);
    },
    titleValidation() {
      this.titleValidate();
    },
    keywordValidation() {
      this.keywordValidate();
    },
    temporalCoverageFromValidation() {
      this.temporalCoverageFromValidate();
    },
    temporalCoverageToValidation() {
      this.temporalCoverageToValidate();
    },
    northBoundingCoordinateValidation() {
      this.northBoundingCoordinateValidate();
    },
    southBoundingCoordinateValidation() {
      this.southBoundingCoordinateValidate();
    },
    eastBoundingCoordinateValidation() {
      this.eastBoundingCoordinateValidate();
    },
    westBoundingCoordinateValidation() {
      this.westBoundingCoordinateValidate();
    },
    locationsValidation() {
      this.locationsValidate();
    },
    taxaCoveredValidation() {
      this.taxaCoveredValidate();
    },
    collectionMethodsValidation() {
      this.collectionMethodValidate();
    },
    dataSourceValidation() {
      this.dataSourceValidate();
    },
    custodianValidation() {
      this.custodianValidate();
    },
    contactOrganisationValidation() {
      this.contactOrganisationValidate();
    },
    contactPositionValidation() {
      this.contactPositionValidate();
    },
    contactEmailValidation() {
      this.contactEmailValidate();
    },
    storedFormatValidation() {
      this.storedFormatValidate();
    },
    availableFormatsValidation() {
      this.availableFormatsValidate();
    },
    accessRightsValidation() {
      this.accessRightsValidate();
    },
    useRestrictionsValidation() {
      this.useRestrictionsValidate();
    },
    securityClassificationValidation() {
      this.securityClassificationValidate();
    },
    generalisationsValidation() {
      this.generalisationsValidate();
    },
  },
  methods: {
    setEditMode() {
      this.editMode = true;
    },
    async getMetadata() {
      this.loading = true;
      this.metadata = await getMetadataAPI(this.$route.params.id);
      this.loading = false;
    },
    formatDate(date) {
      if (date === null) {
        return date;
      }
      if (date === '') {
        return null;
      }
      return date.toISOString().split('T')[0];
    },
    titleValidate() {
      this.titleValidation = titleValidator(this.metadata.title);
    },
    keywordValidate() {
      this.$nextTick(() => {
        this.keywordValidation = keywordsValidator(this.metadata.keywords);
      });
    },
    temporalCoverageFromValidate() {
      this.temporalCoverageFromValidation = temporalCoverageFromValidator(this.metadata.temporal_coverage_from);
    },
    temporalCoverageToValidate() {
      this.temporalCoverageToValidation = temporalCoverageToValidator(this.metadata.temporal_coverage_to);
    },
    northBoundingCoordinateValidate() {
      this.northBoundingCoordinateValidation = northCoordinateValidator(
        this.metadata.north_bounding_coordinate.toString()
      );
    },
    southBoundingCoordinateValidate() {
      this.southBoundingCoordinateValidation = southCoordinateValidator(
        this.metadata.south_bounding_coordinate.toString()
      );
    },
    eastBoundingCoordinateValidate() {
      this.eastBoundingCoordinateValidation = eastCoordinateValidator(
        this.metadata.east_bounding_coordinate.toString()
      );
    },
    westBoundingCoordinateValidate() {
      this.westBoundingCoordinateValidation = westCoordinateValidator(
        this.metadata.west_bounding_coordinate.toString()
      );
    },
    locationsValidate() {
      this.$nextTick(() => {
        this.locationsValidation = locationsValidator(this.metadata.locations);
      });
    },
    taxaCoveredValidate() {
      this.taxaCoveredValidation = taxaValidator(this.metadata.taxa_covered);
    },
    collectionMethodValidate() {
      this.$nextTick(() => {
        this.collectionMethodsValidation = collectionValidator(this.metadata.collection_methods);
      });
    },
    dataSourceValidate() {
      this.dataSourceValidation = dataSourceValidator(this.metadata.data_source_doi, this.metadata.data_source_url);
    },
    custodianValidate() {
      this.custodianValidation = custodianValidator(this.metadata.custodian);
    },
    contactOrganisationValidate() {
      this.contactOrganisationValidation = contactOrgValidator(this.metadata.contact_organisation);
    },
    contactPositionValidate() {
      this.contactPositionValidation = contactPositionValidator(this.metadata.contact_position);
    },
    contactEmailValidate() {
      this.contactEmailValidation = emailValidator(this.metadata.contact_email);
    },
    storedFormatValidate() {
      this.$nextTick(() => {
        this.storedFormatValidation = storedFormatValidator(this.metadata.stored_format);
      });
    },
    availableFormatsValidate() {
      this.$nextTick(() => {
        this.availableFormatsValidation = availableFormatsValidator(this.metadata.available_formats);
      });
    },
    accessRightsValidate() {
      this.$nextTick(() => {
        this.accessRightsValidation = accessRightsValidator(this.metadata.access_rights);
      });
    },
    useRestrictionsValidate() {
      this.useRestrictionsValidation = useRestrictionsValidator(this.metadata.use_restrictions);
    },
    securityClassificationValidate() {
      this.$nextTick(() => {
        this.securityClassificationValidation = securityClassificationValidator(this.metadata.security_classification);
      });
    },
    generalisationsValidate() {
      this.generalisationsValidation = generalisationsValidator(this.metadata.generalisations);
    },
    abstractValidate() {
      this.abstractValidation = abstractValidator(this.metadata.abstract);
    },
    async editMetadata() {
      const { oruga } = useProgrammatic();
      this.loading = true;
      this.notification = await editMetadataAPI(
        this.metadata.id,
        this.metadata.title,
        this.metadata.abstract === null ? '' : this.metadata.abstract,
        this.metadata.keywords,
        this.formatDate(this.metadata.temporal_coverage_from),
        this.formatDate(this.metadata.temporal_coverage_to),
        this.metadata.north_bounding_coordinate,
        this.metadata.south_bounding_coordinate,
        this.metadata.east_bounding_coordinate,
        this.metadata.west_bounding_coordinate,
        this.metadata.location,
        this.metadata.taxa_covered,
        this.metadata.collection_methods,
        this.metadata.data_source,
        this.metadata.embargoed,
        this.formatDate(this.metadata.embargo_release_date),
        this.metadata.custodian,
        this.metadata.contact_organisation,
        this.metadata.contact_position,
        this.metadata.contact_email,
        this.metadata.stored_format,
        this.metadata.available_formats,
        this.metadata.access_rights,
        this.metadata.use_restrictions,
        this.metadata.security_classification,
        this.metadata.generalisations
      );
      this.loading = false;
      this.editMode = false;
      if (this.notification) {
        oruga.notification.open({
          duration: 10000,
          message: this.notification[0],
          variant: this.notification[1] ? 'success' : 'danger',
          position: 'top',
          closable: true,
        });
      }

      setTimeout(() => {
        this.$router.go(0);
      }, 3000);
    },
    async getOptions() {
      this.loading = true;
      this.accessRightsOptions = await getAccessRightsAPI();
      this.collectionMethodsOptions = await getCollectionMethodsAPI();
      this.formatsOptions = await getFormatsAPI();
      this.keywordsOptions = await getKeywordsAPI();
      this.locationsOptions = await getLocationsAPI();
      this.securityClassificationOptions = await getSecurityClassificationsAPI();
      this.loading = false;
    },
    confirmDelete() {
      if (
        confirm(`Are you sure you want to delete the metadata "${this.metadata.title}"? This action cannot be undone.`)
      ) {
        this.deleteMetadata();
      }
    },
    async deleteMetadata() {
      const { oruga } = useProgrammatic();
      this.loading = true;

      try {
        const response = await deleteMetadataAPI(this.metadata.id);
        this.loading = false;

        if (response[1]) {
          oruga.notification.open({
            duration: 5000,
            message: response[0],
            variant: 'success',
            position: 'top',
            closable: true,
          });

          this.$router.push('/metadata');
        } else {
          oruga.notification.open({
            duration: 10000,
            message: response[0],
            variant: 'danger',
            position: 'top',
            closable: true,
          });
        }
      } catch (error) {
        this.loading = false;
        oruga.notification.open({
          duration: 10000,
          message: 'An error occurred while deleting the metadata.',
          variant: 'danger',
          position: 'top',
          closable: true,
        });
      }
    },
  },
};
</script>

<style scoped></style>
