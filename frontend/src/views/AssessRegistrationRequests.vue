<template>
  <PageHeadingWithDescription
    :pageTitle="'Registration Requests'"
    :pageDescription="`${organisationName}`"
    :extraDescription="`${organisationEmail}`" />
  <div class="container">
    <RegistrationRequestApproval
      v-if="selected"
      :id="selected.id"
      :givenName="selected.givenName"
      :familyName="selected.familyName"
      :username="selected.username"
      :organisationId="selected.organisation?.id"
      :organisationABN="selected.organisation?.abn"
      :organisationName="selected.organisation?.name"
      :organisationEmail="selected.organisation?.email"
      :agreements="selected.agreements"
      :group="selected.group"
      :status="selected.status"
      @back="setSelected(undefined, true)" />
    <div v-else class="section">
      <o-loading :active="loading" />

      <div class="columns is-flex is-justify-content-space-between">
        <div class="column buttons is-left">
          <o-field label="Filter by Status:">
            <o-select v-model="statusFilter">
              <option value="">Show all</option>
              fix
              <option value="New">New</option>
              <option value="Approved">Approved</option>
              <option value="Declined">Declined</option>
            </o-select>
          </o-field>
        </div>
        <div class="buttons is-right">
          <div id="pagination-limit">
            <o-select v-model="count">
              <option value="10">10 per page</option>
              <option value="20">20 per page</option>
              <option value="30">30 per page</option>
              <option value="50">50 per page</option>
            </o-select>
          </div>
          <div class="buttons pt-4 pl-4 pr-6">
            <o-button icon-pack="fas" @click="page = page - 1" :disabled="page === 0" aria-label="previous page"
              ><font-awesome-icon icon="fa-solid fa-angle-left"
            /></o-button>
            <o-button
              icon-pack="fas"
              @click="page = page + 1"
              :disabled="final_page && page != 0"
              aria-label="next-page"
              ><font-awesome-icon icon="fa-solid fa-angle-right"
            /></o-button>
          </div>
          <button class="button is-primary ml-6" @click="$router.push('/tools')">Back</button>
        </div>
      </div>

      <o-table v-if="registrations" :loading="loading" :data="registrations" hoverable>
        <o-table-column v-for="column in columns" v-bind="column" #default="{ row }" :visible="column.display">
          <a v-if="column.field === 'id'" @click="setSelected(row, false)">
            {{ row[column.field] }}
          </a>
          <template v-else-if="column.field === 'organisation'">
            {{ typeof row[column.field] === 'string' ? row[column.field] : `${row[column.field].name}` }}
          </template>
          <template v-else-if="column.field === 'createdAt'">
            {{ row.createdAt ? new Date(row.createdAt).toLocaleDateString('en-AU') : '' }}
          </template>
          <template v-else>
            {{ Array.isArray(row[column.field]) ? row[column.field].join(', ') : row[column.field] }}
          </template>
        </o-table-column>
        <o-table-column label="" #default="{ row }">
          <!-- Approved registrations have a Cognito user, so they cannot be deleted here -->
          <o-button
            v-if="[RegistrationStatus.NEW, RegistrationStatus.DECLINED].includes(row.status)"
            variant="danger"
            size="small"
            outlined
            :disabled="loading"
            @click="confirmDelete(row)"
            aria-label="delete registration"
            ><font-awesome-icon icon="fa-solid fa-trash"
          /></o-button>
        </o-table-column>
      </o-table>
      <h2 v-if="!registrations">Not Available</h2>
    </div>
  </div>
</template>

<script lang="ts">
import { deleteRegistrationAPI, getOrganisationsAPI, getRegistrationsAPI } from '@/api/api';
import { defineComponent } from 'vue';
import { useProgrammatic } from '@oruga-ui/oruga-next';
import type { Registration, CreateOrganisation } from '@/api/api.types';
import { RegistrationStatus } from '@/api/api.types';
import PageHeadingWithDescription from '@/components/PageHeadingWithDescription.vue';
import RegistrationRequestApproval from '@/views/RegistrationRequestApproval.vue';
import { useUserDataStore } from '@/store';

interface RegistrationRequestsState {
  loading: boolean;
  registrations: Registration[] | undefined;
  columns: { label: string; field: keyof Registration; display?: boolean }[];
  selected: Registration | undefined;
  count: number;
  currentCursor: string | undefined;
  previousCursors: string[] | undefined[];
  page: number;
  finalPageHit: boolean;
  organisationABN: string;
  organisationName: string;
  organisationEmail: string;
  statusFilter: string | undefined;
}

export default defineComponent({
  name: 'AssessRegistrationRequests',
  components: {
    PageHeadingWithDescription,
    RegistrationRequestApproval,
  },
  data(): RegistrationRequestsState {
    return {
      loading: false,
      registrations: undefined,
      currentCursor: undefined,
      columns: [
        { label: 'Registration Request ID', field: 'id' },
        { label: 'Date Submitted', field: 'createdAt' },
        { label: 'Surname', field: 'familyName' },
        { label: 'Organisation', field: 'organisation' },
        { label: 'Status', field: 'status' },
        // Only used to pass to request approval component
        { label: 'First name', field: 'status', display: false },
        { label: 'Email', field: 'status', display: false },
      ],
      selected: undefined as Registration | undefined,
      count: 20,
      previousCursors: [],
      page: 0,
      finalPageHit: false,
      organisationABN: '',
      organisationName: '',
      organisationEmail: '',
      statusFilter: '',
    };
  },
  mounted() {
    const userStore = useUserDataStore();
    this.organisationABN = userStore.organisationABN || '';
    this.organisationName = userStore.organisationName || '';
    this.organisationEmail = userStore.organisationEmail || '';
    this.getRegistrations(this.count, this.currentCursor, this.statusFilter);
  },
  watch: {
    registrations() {
      this.loading = false;
    },
    count() {
      this.previousCursors = [];
      this.currentCursor = undefined;
      this.page = 0;
      this.finalPageHit = false;
      this.getRegistrations(this.count, this.currentCursor, this.statusFilter);
    },
    statusFilter() {
      this.previousCursors = [];
      this.currentCursor = undefined;
      this.page = 0;
      this.finalPageHit = false;
      this.getRegistrations(this.count, this.currentCursor, this.statusFilter);
    },
    page(newPage, oldPage) {
      if (newPage > oldPage) {
        if (!this.finalPageHit || !this.previousCursors.includes(this.currentCursor)) {
          this.previousCursors.push(this.currentCursor);
        }
        this.getRegistrations(this.count, this.currentCursor, this.statusFilter);
        if (this.final_page) {
          this.finalPageHit = true;
        }
      } else {
        this.getRegistrations(this.count, this.previousCursors[newPage - 1], this.statusFilter);
      }
    },
  },
  computed: {
    RegistrationStatus() {
      return RegistrationStatus;
    },
    visibleColumns() {
      return this.columns.filter((column) => column.display);
    },
    final_page() {
      return !this.currentCursor;
    },
  },
  methods: {
    async getRegistrations(count: number, cursor: string | undefined, statusFilter: string | undefined) {
      this.loading = true;
      if (statusFilter === '') {
        statusFilter = undefined;
      }
      const [registrationsResponse, organisationsResponse] = await Promise.all([
        getRegistrationsAPI(count, cursor, statusFilter),
        getOrganisationsAPI(),
      ]);
      if (registrationsResponse.data) {
        let { results: registrations, cursor } = registrationsResponse.data;
        const organisations = await organisationsResponse;
        registrations.forEach((registration: unknown, index: number) => {
          const organisation = registrations[index].organisation;
          const id = typeof organisation === 'string' ? organisation : undefined;
          let resolvedOrganisation: Partial<CreateOrganisation>;
          if (id) {
            resolvedOrganisation = organisations.find((org) => org.id === id);
          } else {
            resolvedOrganisation = { id: undefined, ...(organisation as CreateOrganisation) };
          }
          registrations[index].organisation = resolvedOrganisation as CreateOrganisation;
        });
        // Sort by createdAt descending
        registrations = registrations.sort((a, b) => {
          const dateA = new Date(a.createdAt).getTime();
          const dateB = new Date(b.createdAt).getTime();
          return dateB - dateA;
        });
        this.registrations = registrations;
        this.currentCursor = cursor;
      }
    },
    setSelected(selected: Registration | undefined, refresh: boolean) {
      this.selected = selected;
      if (refresh) {
        this.getRegistrations(this.count, this.currentCursor, this.statusFilter);
      }
    },
    confirmDelete(registration: Registration) {
      if (
        confirm(
          `Are you sure you want to delete the ${registration.status.toLowerCase()} registration request for ${
            registration.givenName
          } ${registration.familyName} (${registration.username})? This action cannot be undone.`
        )
      ) {
        this.deleteRegistration(registration);
      }
    },
    async deleteRegistration(registration: Registration) {
      this.loading = true;
      const response = await deleteRegistrationAPI(registration.id);
      this.loading = false;
      const { oruga } = useProgrammatic();
      const message = response.error
        ? response.error.message
        : `Registration request for ${registration.givenName} ${registration.familyName} was successfully deleted.`;
      oruga.notification.open({
        message: message,
        position: 'top',
        closable: true,
        variant: response.error ? 'danger' : 'success',
        duration: 10000,
      });
      if (!response.error) {
        // Reload the current page (`currentCursor` points to the next page)
        this.getRegistrations(this.count, this.previousCursors[this.page - 1], this.statusFilter);
      }
    },
  },
});
</script>

<style scoped>
#pagination-limit {
  margin-bottom: 8px;
  margin-left: 20px;
}

.input {
  width: 50%;
}
</style>
