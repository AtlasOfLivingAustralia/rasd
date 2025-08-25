<template>
  <PageHeading pageTitle="Add Metadata" />
  <div class="container">
    <div class="section">
      <router-link to="/metadata">Go Back</router-link>
      <div class="field pt-5">
        <o-field
          class="label"
          :variant="this.titleValidation.titleClasses === 'is-danger' ? 'danger' : ''"
          :message="this.titleValidation.titleClasses === 'is-danger' ? 'Title must not be empty' : ''"
          >* Title:</o-field
        >
        <o-input
          v-model="title"
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
          v-model="abstract"
          :class="this.abstractValidation.abstractClasses"
          maxlength="500"
          @blur="this.abstractValidate"></o-input>
      </div>
      <div class="field">
        <o-field
          class="label"
          :variant="this.keywordValidation.keywordClasses === 'is-danger' ? 'danger' : ''"
          :message="this.keywordValidation.keywordClasses === 'is-danger' ? 'Keywords must not be empty' : ''"
          >* Keywords:</o-field
        >
        <o-dropdown v-if="keywordsOptions" v-model="keywords" @change="this.keywordValidate" multiple role="list">
          <template #trigger>
            <o-button variant="primary" :class="this.keywordValidation.keywordClasses" type="button">
              <span v-if="keywords">
                {{ keywords_text }}
                <span v-if="keywords.length > 8">...</span>
              </span>
              <span v-else>Please select keywords </span>
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
          :class="this.temporalCoverageFromValidation.temporalCoverageFromClasses"
          v-model="temporal_coverage_from"
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
          v-model="temporal_coverage_to"
          :class="this.temporalCoverageToValidation.temporalCoverageToClasses"
          @blur="this.temporalCoverageToValidate"
          :min-date="minDate"></o-datepicker>
      </div>
      <div class="field">
        <o-field
          class="label"
          :message="
            this.northBoundingCoordinateValidation.northBoundingCoordinateClasses !== 'is-danger'
              ? 'Please enter your value as an integer'
              : 'North Bounding Coordinate must be an integer value from -90 and 90 inclusive. Bounding coordinates must not be empty.'
          "
          :variant="
            this.northBoundingCoordinateValidation.northBoundingCoordinateClasses === 'is-danger' ? 'danger' : ''
          "
          >* North Bounding Coordinate:</o-field
        >
        <o-input
          v-model="north_bounding_coordinate"
          :class="this.northBoundingCoordinateValidation.northBoundingCoordinateClasses"
          @blur="this.northBoundingCoordinateValidate"
          placeholder="e.g. 90"></o-input>
      </div>
      <div class="field">
        <o-field
          class="label"
          :message="
            this.southBoundingCoordinateValidation.southBoundingCoordinateClasses !== 'is-danger'
              ? 'Please enter your value as an integer'
              : 'South Bounding Coordinate must be an integer value from -90 and 90 inclusive. Bounding coordinates must not be empty.'
          "
          :variant="
            this.southBoundingCoordinateValidation.southBoundingCoordinateClasses === 'is-danger' ? 'danger' : ''
          "
          >* South Bounding Coordinate:</o-field
        >
        <o-input
          v-model="south_bounding_coordinate"
          :class="this.southBoundingCoordinateValidation.southBoundingCoordinateClasses"
          @blur="this.southBoundingCoordinateValidate"
          placeholder="e.g. 90"></o-input>
      </div>
      <div class="field">
        <o-field
          class="label"
          :message="
            this.eastBoundingCoordinateValidation.eastBoundingCoordinateClasses !== 'is-danger'
              ? 'Please enter your value as an integer'
              : 'East Bounding Coordinate must be an integer value from -180 and 180 inclusive. Bounding coordinates must not be empty.'
          "
          :variant="this.eastBoundingCoordinateValidation.eastBoundingCoordinateClasses === 'is-danger' ? 'danger' : ''"
          >* East Bounding Coordinate:</o-field
        >
        <o-input
          v-model="east_bounding_coordinate"
          :class="this.eastBoundingCoordinateValidation.eastBoundingCoordinateClasses"
          @blur="this.eastBoundingCoordinateValidate"
          placeholder="e.g. 180"></o-input>
      </div>
      <div class="field">
        <o-field
          class="label"
          :message="
            this.westBoundingCoordinateValidation.westBoundingCoordinateClasses !== 'is-danger'
              ? 'Please enter your value as an integer'
              : 'West Bounding Coordinate must be an integer value from -180 and 180 inclusive. Bounding coordinates must not be empty.'
          "
          :variant="this.westBoundingCoordinateValidation.westBoundingCoordinateClasses === 'is-danger' ? 'danger' : ''"
          >* West Bounding Coordinate:</o-field
        >
        <o-input
          v-model="west_bounding_coordinate"
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
        <o-dropdown v-if="locationsOptions" v-model="locations" multiple ole="list" @change="this.locationsValidate">
          <template #trigger>
            <o-button variant="primary" :class="this.locationsValidation.locationsClasses" type="button">
              <span v-if="locations"> {{ locations_text }}<span v-if="locations.length > 7">...</span> </span>
              <span v-else>Please select locations</span>
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
          v-model="taxa_covered"
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
        <o-dropdown v-model="collection_methods" @change="this.collectionMethodValidate" multiple role="list">
          <template #trigger>
            <o-button variant="primary" type="button" :class="collectionMethodsValidation.collectionMethodsClasses">
              <span>{{ collection_methods_text }}</span>
            </o-button>
          </template>
          <o-dropdown-item v-for="collection_method in collectionMethodsOptions" :value="collection_method">{{
            collection_method
          }}</o-dropdown-item>
        </o-dropdown>
      </div>
      <p class="pt-2 label">You must add at least the Data Source DOI or the Data Source URL</p>
      <div class="field">
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
          placeholder="e.g. 10.1000/182"
          v-model="data_source_doi"
          :class="this.dataSourceValidation.dataSourceDOIClasses"
          @blur="this.dataSourceValidate"></o-input>
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
          placeholder="https://www.example.com.au"
          v-model="data_source_url"
          :class="this.dataSourceValidation.dataSourceURLClasses"
          @blur="this.dataSourceValidate"></o-input>
      </div>
      <div class="field">
        <o-field class="label">* Embargoed:</o-field>
        <o-select v-model="embargoed">
          <option value="true">True</option>
          <option value="false">False</option>
        </o-select>
      </div>
      <div v-if="embargoed === 'true'" class="field">
        <o-field class="label">Embargo Release Date: (Optional)</o-field>
        <o-datepicker v-model="embargo_release_date"></o-datepicker>
      </div>
      <div class="field">
        <o-field class="label">* Custodian Organisation:</o-field>
        <o-input type="text" v-model="custodianOrganisation" :disabled="true"> </o-input>
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
          v-model="contact_organisation"
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
          v-model="contact_position"
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
          v-model="contact_email"
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
        <o-dropdown v-model="stored_format" @change="this.storedFormatValidate">
          <template #trigger>
            <o-button variant="primary" type="button" :class="this.storedFormatValidation.storedFormatClasses">
              <span>{{ stored_format ? stored_format : 'Select a stored format' }}</span>
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
        <o-dropdown v-model="available_formats" multiple role="list" @change="this.availableFormatsValidate">
          <template #trigger>
            <o-button variant="primary" :class="this.availableFormatsValidation.availableFormatsClasses" type="button">
              <span>{{ available_formats_text }}</span>
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
        <o-dropdown v-model="access_rights" @change="this.accessRightsValidate">
          <template #trigger>
            <o-button variant="primary" :class="this.accessRightsValidation.accessRightsClasses">
              <span>{{ access_rights ? access_rights : 'Please select an access right' }}</span>
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
          v-model="use_restrictions"
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
        <o-dropdown v-model="security_classification" @change="this.securityClassificationValidate">
          <template #trigger>
            <o-button variant="primary" :class="this.securityClassificationValidation.securityClassificationClasses">
              <span>{{ security_classification ? security_classification : 'Select a security classification' }}</span>
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
          v-model="generalisations"
          :class="this.generalisationsValidation.generalisationsClasses"
          @blur="this.generalisationsValidate"
          maxlength="500"
          placeholder="Any rulesets which have been applied at a dataset level to obfuscate or generalise either species attributes or location or remove/modify personal identifiable information"></o-input>
      </div>
      <div class="field is-grouped">
        <o-button
          class="button"
          variant="success"
          :class="{ 'is-loading': this.loading }"
          :disabled="canSubmitForm || this.loading"
          @click="this.createMetadata"
          >Add</o-button
        >
      </div>
    </div>
  </div>
</template>

<script>
import PageHeading from '../components/PageHeading.vue';
import {
  createMetadataAPI,
  getAccessRightsAPI,
  getCollectionMethodsAPI,
  getFormatsAPI,
  getKeywordsAPI,
  getLocationsAPI,
  getSecurityClassificationsAPI,
} from '../api/api';
import {
  abstractValidator,
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
} from '@/helpers/helpers';
import { useProgrammatic } from '@oruga-ui/oruga-next';
import { useUserDataStore } from '@/store';

export default {
  name: 'MetadataView',
  components: {
    PageHeading,
  },
  beforeMount() {
    this.getOptions();
  },
  computed: {
    canSubmitForm() {
      return !(
        this.titleValidation.valid &&
        this.abstractValidation.valid &&
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
        this.contactOrganisationValidation.valid &&
        this.contactPositionValidation.valid &&
        this.contactEmailValidation.valid &&
        this.storedFormatValidation.valid &&
        this.availableFormatsValidation.valid &&
        this.accessRightsValidation.valid &&
        this.useRestrictionsValidation.valid &&
        this.securityClassificationValidation.valid &&
        this.generalisationsValidation.valid
      );
    },
    available_formats_text() {
      if (this.available_formats.length === 0) {
        return 'Select an available format';
      } else {
        return this.available_formats.toString();
      }
    },
    keywords_text() {
      if (this.keywords.length === 0) {
        return 'Select a keyword';
      } else {
        return this.keywords.slice(0, 8).join(', ').toString();
      }
    },
    locations_text() {
      if (this.locations.length === 0) {
        return 'Select a location';
      } else {
        return this.locations.slice(0, 7).join(', ').toString();
      }
    },
    collection_methods_text() {
      if (this.collection_methods.length === 0) {
        return 'Select a collection method';
      } else {
        return this.collection_methods.join(', ').toString();
      }
    },
  },
  data() {
    return {
      title: '',
      titleValidation: {
        valid: false,
        titleClasses: '',
      },
      abstract: '',
      abstractValidation: {
        valid: false,
        abstractClasses: '',
      },
      keywords: null,
      keywordValidation: {
        valid: false,
        keywordClasses: '',
      },
      temporal_coverage_from: null,
      temporalCoverageFromValidation: {
        valid: false,
        temporalCoverageFromClasses: '',
      },
      temporal_coverage_to: null,
      temporalCoverageToValidation: {
        valid: false,
        temporalCoverageToClasses: '',
      },
      north_bounding_coordinate: null,
      northBoundingCoordinateValidation: {
        valid: false,
        northBoundingCoordinateClasses: '',
      },
      south_bounding_coordinate: null,
      southBoundingCoordinateValidation: {
        valid: false,
        southBoundingCoordinateClasses: '',
      },
      east_bounding_coordinate: null,
      eastBoundingCoordinateValidation: {
        valid: false,
        eastBoundingCoordinateClasses: '',
      },
      west_bounding_coordinate: null,
      westBoundingCoordinateValidation: {
        valid: false,
        westBoundingCoordinateClasses: '',
      },
      locations: null,
      locationsValidation: {
        valid: false,
        locationsClasses: '',
      },
      taxa_covered: '',
      taxaCoveredValidation: {
        valid: false,
        taxaCoveredClasses: '',
      },
      collection_methods: [],
      collectionMethodsValidation: {
        valid: false,
        collectionMethodsClasses: '',
      },
      data_source_doi: '',
      data_source_url: '',
      dataSourceValidation: {
        valid: false,
        dataSourceDOIValidation: {
          valid: false,
          dataSourceDOIClasses: '',
        },
        dataSourceURLValidation: {
          valid: false,
          dataSourceURLClasses: '',
        },
      },
      embargoed: false,
      embargo_release_date: null,
      custodianValidation: {
        valid: false,
        custodianClasses: '',
      },
      custodianOrganisation: this.getCustodianOrganisation(),
      contact_organisation: '',
      contactOrganisationValidation: {
        valid: false,
        contactOrganisationClasses: '',
      },
      contact_position: '',
      contactPositionValidation: {
        valid: false,
        contactPositionClasses: '',
      },
      contact_email: '',
      contactEmailValidation: {
        valid: false,
        emailClasses: '',
      },
      stored_format: '',
      storedFormatValidation: {
        valid: false,
        storedFormatClasses: '',
      },
      available_formats: [],
      availableFormatsValidation: {
        valid: false,
        availableFormatsClasses: '',
      },
      access_rights: '',
      accessRightsValidation: {
        valid: false,
        accessRightsClasses: '',
      },
      use_restrictions: '',
      useRestrictionsValidation: {
        valid: false,
        useRestrictionsClasses: '',
      },
      security_classification: '',
      securityClassificationValidation: {
        valid: false,
        securityClassificationClasses: '',
      },
      generalisations: '',
      generalisationsValidation: {
        valid: false,
        generalisationsClasses: '',
      },
      collectionMethodsOptions: [],
      formatsOptions: [],
      keywordsOptions: [],
      locationsOptions: [],
      securityClassificationOptions: [],
      accessRightsOptions: [],
      notification: null,
      minDate: new Date('1760-01-01'),
      loading: false,
    };
  },
  watch: {
    embargoed() {
      if (this.embargoed === 'false') {
        this.embargo_release_date = null;
      }
    },
  },
  methods: {
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
    formatDate(date) {
      if (date === null) {
        return date;
      }
      return date.toISOString().split('T')[0];
    },
    getCustodianOrganisation() {
      const userStore = useUserDataStore();
      if (userStore.organisationName) {
        return userStore.organisationName;
      }
      this.$router.push('/login');
    },
    titleValidate() {
      this.titleValidation = titleValidator(this.title);
    },
    abstractValidate() {
      this.abstractValidation = abstractValidator(this.abstract);
    },
    keywordValidate() {
      this.$nextTick(() => {
        this.keywordValidation = keywordsValidator(this.keywords);
      });
    },
    temporalCoverageFromValidate() {
      this.temporalCoverageFromValidation = temporalCoverageFromValidator(this.temporal_coverage_from);
    },
    temporalCoverageToValidate() {
      this.temporalCoverageToValidation = temporalCoverageToValidator(this.temporal_coverage_to);
    },
    northBoundingCoordinateValidate() {
      this.northBoundingCoordinateValidation = northCoordinateValidator(this.north_bounding_coordinate);
    },
    southBoundingCoordinateValidate() {
      this.southBoundingCoordinateValidation = southCoordinateValidator(this.south_bounding_coordinate);
    },
    eastBoundingCoordinateValidate() {
      this.eastBoundingCoordinateValidation = eastCoordinateValidator(this.east_bounding_coordinate);
    },
    westBoundingCoordinateValidate() {
      this.westBoundingCoordinateValidation = westCoordinateValidator(this.west_bounding_coordinate);
    },
    locationsValidate() {
      this.$nextTick(() => {
        this.locationsValidation = locationsValidator(this.locations);
      });
    },
    taxaCoveredValidate() {
      this.taxaCoveredValidation = taxaValidator(this.taxa_covered);
    },
    collectionMethodValidate() {
      this.$nextTick(() => {
        this.collectionMethodsValidation = collectionValidator(this.collection_methods);
      });
    },
    dataSourceValidate() {
      this.dataSourceValidation = dataSourceValidator(this.data_source_doi, this.data_source_url);
    },
    custodianValidate() {
      this.custodianValidation = custodianValidator(this.custodian);
    },
    contactOrganisationValidate() {
      this.contactOrganisationValidation = contactOrgValidator(this.contact_organisation);
    },
    contactPositionValidate() {
      this.contactPositionValidation = contactPositionValidator(this.contact_position);
    },
    contactEmailValidate() {
      this.contactEmailValidation = emailValidator(this.contact_email);
    },
    storedFormatValidate() {
      this.$nextTick(() => {
        this.storedFormatValidation = storedFormatValidator(this.stored_format);
      });
    },
    availableFormatsValidate() {
      this.$nextTick(() => {
        this.availableFormatsValidation = availableFormatsValidator(this.available_formats);
      });
    },
    accessRightsValidate() {
      this.$nextTick(() => {
        this.accessRightsValidation = accessRightsValidator(this.access_rights);
      });
    },
    useRestrictionsValidate() {
      this.useRestrictionsValidation = useRestrictionsValidator(this.use_restrictions);
    },
    securityClassificationValidate() {
      this.$nextTick(() => {
        this.securityClassificationValidation = securityClassificationValidator(this.security_classification);
      });
    },
    generalisationsValidate() {
      this.generalisationsValidation = generalisationsValidator(this.generalisations);
    },
    async createMetadata() {
      const { oruga } = useProgrammatic();
      this.loading = true;
      this.notification = await createMetadataAPI(
        this.title,
        this.abstract,
        this.keywords,
        this.formatDate(this.temporal_coverage_from),
        this.formatDate(this.temporal_coverage_to),
        this.north_bounding_coordinate,
        this.south_bounding_coordinate,
        this.east_bounding_coordinate,
        this.west_bounding_coordinate,
        this.locations,
        this.taxa_covered,
        this.collection_methods,
        this.data_source_url,
        this.data_source_doi,
        this.embargoed,
        this.formatDate(this.embargo_release_date),
        this.contact_organisation,
        this.contact_position,
        this.contact_email,
        this.stored_format,
        this.available_formats,
        this.access_rights,
        this.use_restrictions,
        this.security_classification,
        this.generalisations
      );
      this.loading = false;
      if (this.notification) {
        oruga.notification.open({
          message: this.notification[0],
          position: 'top',
          closable: true,
          variant: this.notification[1] ? 'success' : 'danger',
          duration: 10000,
        });
        if (this.notification[1]) {
          return this.clearFields();
        }
      }
    },
    clearFields() {
      this.title = '';
      this.titleValidation = {
        valid: false,
        titleClasses: '',
      };
      this.abstract = '';
      this.keywords = '';
      this.keywordValidation = {
        valid: false,
        keywordsClasses: '',
      };
      this.temporal_coverage_from = null;
      this.temporalCoverageFromValidation = {
        valid: false,
        temporalCoverageFromClasses: '',
      };
      this.temporal_coverage_to = null;
      this.temporalCoverageToValidation = {
        valid: false,
        temporalCoverageToClasses: '',
      };
      this.north_bounding_coordinate = '';
      this.northBoundingCoordinateValidation = {
        valid: false,
        northBoundingCoordinateClasses: '',
      };
      this.south_bounding_coordinate = '';
      this.southBoundingCoordinateValidation = {
        valid: false,
        southBoundingCoordinateClasses: '',
      };
      this.east_bounding_coordinate = '';
      this.eastBoundingCoordinateValidation = {
        valid: false,
        eastBoundingCoordinateClasses: '',
      };
      this.west_bounding_coordinate = '';
      this.westBoundingCoordinateValidation = {
        valid: false,
        westBoundingCoordinateClasses: '',
      };
      this.locations = '';
      this.locationsValidation = {
        valid: false,
        locationsClasses: '',
      };
      this.taxa_covered = '';
      this.taxaCoveredValidation = {
        valid: false,
        taxaCoveredClasses: '',
      };
      this.collection_methods = '';
      this.collectionMethodsValidation = {
        valid: false,
        collectionMethodsClasses: '',
      };
      this.data_source_doi = '';
      this.data_source_url = '';
      this.dataSourceValidation = {
        valid: false,
        dataSourceDOIValidation: {
          valid: false,
          dataSourceDOIClasses: '',
        },
        dataSourceURLValidation: {
          valid: false,
          dataSourceURLClasses: '',
        },
      };
      this.embargoed = false;
      this.embargo_release_date = null;
      this.custodianValidation = {
        custodianClasses: '',
      };
      this.contact_organisation = '';
      this.contactOrganisationValidation = {
        valid: false,
        contactOrganisationClasses: '',
      };
      this.contact_position = '';
      this.contactPositionValidation = {
        valid: false,
        contactPositionClasses: '',
      };
      this.contact_email = '';
      this.contactEmailValidation = {
        valid: false,
        contactEmailClasses: '',
      };
      this.stored_format = '';
      this.storedFormatValidation = {
        valid: false,
        storedFormatClasses: '',
      };
      this.available_formats = '';
      this.access_rights = '';
      this.accessRightsValidation = {
        valid: false,
        accessRightsClasses: '',
      };
      this.use_restrictions = '';
      this.useRestrictionsValidation = {
        valid: false,
        useRestrictionsClasses: '',
      };
      this.security_classification = '';
      this.securityClassificationValidation = {
        valid: false,
        securityClassificationClasses: '',
      };
      this.generalisations = '';
      this.generalisationsValidation = {
        valid: false,
        generalisationsClasses: '',
      };
    },
  },
};
</script>

<style scoped></style>
