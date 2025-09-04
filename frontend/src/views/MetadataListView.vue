<template>
  <PageHeading pageTitle="Metadata / List" />
  <div class="section">
    <o-loading :active="loading" />
    <div>
      <div class="buttons is-right">
        <o-button @click="this.routeToAddMetadata" variant="primary">Add Metadata</o-button>
      </div>
      <div class="buttons is-left">
        <o-dropdown v-model="visibleColumns" multiple>
          <template #trigger>
            <o-button variant="primary" type="button">
              <span>{{ 'Columns' }}</span>
            </o-button>
          </template>
          <o-dropdown-item
            v-for="column in columns"
            scrollable
            :value="column"
            @click="() => changeColumnVisibility(column)"
            >{{ column.label }}</o-dropdown-item
          >
        </o-dropdown>
        <div id="pagination-limit">
          <o-select v-model="count">
            <option value="10">10 per page</option>
            <option value="20">20 per page</option>
            <option value="30">30 per page</option>
            <option value="50">50 per page</option>
          </o-select>
        </div>
      </div>
      <o-table
        v-if="metadata?.results"
        :loading="loading"
        :data="metadata?.results"
        v-model:selected="selected"
        hoverable>
        <o-table-column v-for="column in columns" v-bind="column" #default="{ row }" :visible="column.display">
          {{ Array.isArray(row[column.field]) ? row[column.field].join(', ') : row[column.field] }}
        </o-table-column>
        <o-table-column width="100">
          <!--Exists for visual/ux purposes the click functionality comes from the table-->
          <o-button variant="primary" type="button">View/Edit</o-button>
        </o-table-column>
      </o-table>
      <o-button
        icon-pack="fas"
        @click="this.page = this.page - 1"
        :disabled="this.page === 0"
        aria-label="previous page"
        ><font-awesome-icon icon="fa-solid fa-angle-left"
      /></o-button>
      <o-button icon-pack="fas" @click="this.page = this.page + 1" :disabled="final_page" aria-label="next page"
        ><font-awesome-icon icon="fa-solid fa-angle-right"
      /></o-button>
      <h2 v-if="!metadata">Not Available</h2>
    </div>
  </div>
</template>

<script>
import { getMetadataListAPI } from '../api/api';
import PageHeading from '../components/PageHeading.vue';

export default {
  name: 'MetadataListView',
  components: {
    PageHeading,
  },
  data() {
    return {
      loading: false,
      metadata: null,
      columns: [
        { label: 'Title', field: 'title', display: true },
        { label: 'Abstract', field: 'abstract', display: true },
        { label: 'Keywords', field: 'keywords', display: true },
        { label: 'Temporal Coverage From', field: 'temporal_coverage_from', display: true },
        { label: 'Temporal Coverage To', field: 'temporal_coverage_to', display: true },
        { label: 'North Bounding Coordinate', field: 'north_bounding_coordinate', display: true },
        { label: 'South Bounding Coordinate', field: 'south_bounding_coordinate', display: true },
        { label: 'East Bounding Coordinate', field: 'east_bounding_coordinate', display: true },
        { label: 'West Bounding Coordinate', field: 'west_bounding_coordinate', display: true },
        { label: 'Locations', field: 'locations', display: true },
        { label: 'Taxa Covered', field: 'taxa_covered', display: false },
        { label: 'Collection Methods', field: 'collection_methods', display: false },
        { label: 'Data Source DOI', field: 'data_source_doi', display: false },
        { label: 'Data Source URL', field: 'data_source_url', display: false },
        { label: 'Embargoed', field: 'embargoed', display: false },
        { label: 'Embargo Release Date', field: 'embargo_release_date', display: false },
        { label: 'Custodian', field: 'custodian', display: false },
        { label: 'Contact Organisation', field: 'contact_organisation', display: false },
        { label: 'Contact Position', field: 'contact_position', display: false },
        { label: 'Contact Email', field: 'contact_email', display: false },
        { label: 'Stored Format', field: 'stored_format', display: false },
        { label: 'Available Formats', field: 'available_formats', display: false },
        { label: 'Access Rights', field: 'access_rights', display: false },
        { label: 'Use Restrictions', field: 'use_restrictions', display: false },
        { label: 'Security Classification', field: 'security_classification', display: false },
        { label: 'Generalisations', field: 'generalisations', display: false },
      ],
      selected: null,
      count: 20,
      previousCursors: [''],
      page: 0,
      finalPageHit: false,
    };
  },
  beforeMount() {
    this.getMetadata();
  },
  watch: {
    metadata() {
      this.loading = false;
    },
    selected() {
      this.$router.push(`/metadata/${this.selected.id}`);
    },
    count() {
      this.previousCursors = [''];
      this.page = 0;
      this.finalPageHit = false;
      this.getMetadata(this.count);
    },
    page(newPage, oldPage) {
      if (newPage > oldPage) {
        if (!this.finalPageHit || !this.previousCursors.includes(this.metadata.cursor)) {
          this.previousCursors.push(this.metadata.cursor);
        }
        this.getMetadata(this.count, this.metadata.cursor);
        if (this.final_page) {
          this.finalPageHit = true;
        }
      } else {
        this.getMetadata(this.count, this.previousCursors[newPage]);
      }
    },
  },
  computed: {
    visibleColumns() {
      return this.columns.filter((column) => column.display);
    },
    final_page() {
      return this.metadata?.cursor === null;
    },
  },
  methods: {
    async getMetadata(count = 20, cursor = '') {
      this.loading = true;
      this.metadata = await getMetadataListAPI(count, cursor);
      if (this.metadata?.results) {
        this.metadata.results.sort((a, b) => {
          const titleA = (a.title || '').toLowerCase();
          const titleB = (b.title || '').toLowerCase();
          return titleA.localeCompare(titleB);
        });
      }
    },
    routeToAddMetadata() {
      this.$router.push('/metadata/add');
    },
    changeColumnVisibility(column) {
      column.display = !column.display;
    },
  },
};
</script>

<style scoped>
#pagination-limit {
  margin-bottom: 8px;
  margin-left: 20px;
}
</style>
