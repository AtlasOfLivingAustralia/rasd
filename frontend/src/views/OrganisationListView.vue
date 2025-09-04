<template>
  <PageHeading pageTitle="Organisation / List" />
  <div class="section">
    <o-loading :active="loading" />
    <div>
      <div class="buttons is-right">
        <o-button variant="primary" @click="this.routeToAddOrganisation">Add Organisation</o-button>
      </div>
      <o-table v-if="organisations" :loading="loading" :data="organisations" v-model:selected="selected" hoverable>
        <o-table-column v-for="column in columns" v-bind="column" #default="{ row }">
          {{ row[column.field] }}
        </o-table-column>
        <o-table-column width="100">
          <!--Exists for visual/ux purposes the click functionality comes from the table-->
          <o-button variant="primary" type="button">View/Edit</o-button>
        </o-table-column>
      </o-table>
      <h2 v-if="!organisations">Not Available</h2>
    </div>
  </div>
</template>

<script>
import { getOrganisationsAPI } from '../api/api';
import PageHeading from '../components/PageHeading.vue';

export default {
  name: 'OrganisationListView',
  components: {
    PageHeading,
  },
  data() {
    return {
      loading: false,
      tabulator: null,
      organisations: null,
      columns: [
        { label: 'Name', field: 'name' },
        { label: 'ABN', field: 'abn' },
        { label: 'Email', field: 'email' },
      ],
      selected: null,
    };
  },
  beforeMount() {
    this.getOrganisations();
  },
  watch: {
    organisations() {
      this.loading = false;
    },
    selected() {
      this.$router.push(`/organisations/${this.selected.id}`);
    },
  },
  methods: {
    async getOrganisations() {
      this.loading = true;
      this.organisations = await getOrganisationsAPI();
      if (this.organisations) {
        this.organisations.sort((a, b) => {
          const nameA = (a.name || '').toLowerCase();
          const nameB = (b.name || '').toLowerCase();
          return nameA.localeCompare(nameB);
        });
      }
    },
    routeToAddOrganisation() {
      this.$router.push('/organisations/add');
    },
  },
};
</script>

<style scoped></style>
