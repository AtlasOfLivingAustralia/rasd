<template>
  <PageHeadingWithDescription
    :pageTitle="
      role === UserGroup.DataRequestors
        ? 'Status of Requests'
        : role === UserGroup.DataCustodians
        ? 'Action Data Access Requests'
        : 'All Data Access Requests'
    "
    :pageDescription="`${userData.organisationName}`"
    :extraDescription="`${userData.organisationEmail}`" />
  <div class="container">
    <div class="section">
      <div class="columns is-flex is-justify-content-space-between">
        <div class="column is-flex mr-6">
          <o-field label="Search by ID:" class="pr-6">
            <div class="is-flex is-align-items-left">
              <input
                v-model="idFilter"
                class="input is-normal"
                type="text"
                placeholder="RASD Data Access Request ID"
                maxlength="200" />
              <div class="buttons mx-3">
                <o-button class="button is-secondary" @click="searchById">Search</o-button>
              </div>
              <div class="buttons pb-5">
                <o-button class="button is-primary" @click="clearFilter">Show all results</o-button>
              </div>
            </div>
          </o-field>
        </div>

        <div class="column is-flex is-align-items-center">
          <div class="buttons pt-5 mr-4">
            <o-select v-model="limit">
              <option value="10">10 per page</option>
              <option value="20">20 per page</option>
              <option value="30">30 per page</option>
              <option value="50">50 per page</option>
            </o-select>
          </div>
          <div class="buttons pt-2">
            <o-button
              icon-pack="fas"
              class="button"
              @click="page = page - 1"
              :disabled="page === 0"
              aria-label="previous-page">
              <font-awesome-icon icon="fa-solid fa-angle-left" />
            </o-button>
            <o-button
              icon-pack="fas"
              class="button"
              @click="page = page + 1"
              :disabled="final_page"
              aria-label="next-page">
              <font-awesome-icon icon="fa-solid fa-angle-right" />
            </o-button>
          </div>
        </div>

        <div class="buttons pt-3">
          <button class="button is-primary" @click="goBack">Back</button>
        </div>
      </div>

      <!-- Data Requestor View -->
      <div v-if="role === UserGroup.DataRequestors">
        <div v-for="dataAccessRequest in computedDataAccessRequests" class="card mb-6 mt-6" :key="dataAccessRequest.id">
          <header class="card-header has-background-warning">
            <div
              class="card-header-button w-full card-header-icon py-3 my-4 px-6 has-text-left"
              aria-label="Show all request IDs">
              <table class="header-table">
                <th class="is-size-4 has-text-black">Data Access Request</th>
                <tr>
                  <td class="header-property-column">Data Access Request ID:</td>
                  <td class="header-data-column">{{ dataAccessRequest.id }}</td>
                </tr>
                <tr>
                  <td class="header-property-column">Date Received:</td>
                  <td class="header-data-column">
                    {{ convertToLocalDateTime(dataAccessRequest.datasetRequests[0].audit[0].at) }}
                  </td>
                </tr>
                <tr>
                  <td class="header-property-column">Project Title:</td>
                  <td class="child-data-column">{{ dataAccessRequest.project.title }}</td>
                </tr>
                <tr class="field">
                  <td class="has-text-weight-bold">DOI:</td>
                  <td>
                    <div class="mt-2 mr-4 doi-input">
                      <o-input :disabled="true" v-model="dataAccessRequest.doi"></o-input>
                    </div>
                  </td>
                </tr>
              </table>
              <div class="parent-status">
                <p class="has-text-weight-bold is-size-5">Data Access Request Status:</p>
                <p class="is-size-5">
                  {{ !!dataAccessRequest.completed_at ? 'Complete' : 'Pending' }}
                </p>
                <div class="audit-data" v-if="!!dataAccessRequest.completed_at">
                  <p class="has-text-weight-bold">Completed at:</p>
                  <p>
                    {{ convertToLocalDateTime(dataAccessRequest.completed_at) }}
                  </p>
                </div>
                <div class="mt-6 ml-6">
                  <div>
                    <div
                      v-if="openCollapsibles[dataAccessRequest.id]"
                      class="level-right"
                      @click="toggleCollapsible(dataAccessRequest.id)">
                      <span class="level-item pt-5 is-underlined"
                        >Hide datasets included in this request
                        <font-awesome-icon
                          icon="fa-solid fa-close level-item"
                          class="is-size-3 ml-3"></font-awesome-icon>
                      </span>
                    </div>

                    <div
                      v-if="!openCollapsibles[dataAccessRequest.id]"
                      @click="toggleCollapsible(dataAccessRequest.id)">
                      <span class="level-right is-underlined pt-6 mt-6"
                        >Show datasets included in this request
                        <font-awesome-icon
                          icon="fa-solid fa-angle-down level-item"
                          class="is-size-3 ml-3"></font-awesome-icon
                      ></span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </header>
          <div
            class="card-content has-background-warning-light"
            :class="{ active: openCollapsibles[dataAccessRequest.id] }"
            :data-collapsible-content="dataAccessRequest.id">
            <h4 class="is-size-4 has-text-weight-bold py-2 pl-5 has-text-black">
              Status of datasets included in request ({{ getFilteredDatasetRequests(dataAccessRequest).length }})
            </h4>
            <div
              v-for="datasetRequest in getFilteredDatasetRequests(dataAccessRequest)"
              :key="datasetRequest.id"
              class="dataset-card py-4">
              <a @click="setOpenDatasetRequest(dataAccessRequest.id, datasetRequest.id)">
                <div class="card-button py-4 px-5">
                  <table class="requestor-child-table">
                    <tr>
                      <td class="child-property-column">Dataset Request ID:</td>
                      <td class="child-data-column">{{ datasetRequest.id }}</td>
                    </tr>
                    <tr>
                      <td class="child-property-column">Date Submitted:</td>
                      <td class="child-data-column">
                        {{ convertToLocalDateTime(datasetRequest.audit[0].at) }}
                      </td>
                    </tr>
                    <tr>
                      <td class="child-property-column">Data Custodian:</td>
                      <td class="child-data-column">{{ datasetRequest.custodianName }}</td>
                    </tr>
                    <tr>
                      <td class="child-property-column">Dataset Title:</td>
                      <td class="child-data-column">{{ datasetRequest.metadataTitle }}</td>
                    </tr>
                  </table>
                  <span class="pl-6 ml-6 pb-6">
                    <div class="is-inline-block mr-2 has-text-weight-bold is-size-5">Dataset Status:</div>
                    <div class="is-inline-block is-size-5">
                      {{ datasetRequest.status }}
                    </div>
                    <div class="audit-data is-flex-wrap-wrap">
                      <p class="has-text-weight-bold">Last action:</p>
                      <p>{{ datasetRequest.audit[datasetRequest.audit.length - 1].by }}</p>
                      <p>{{ convertToLocalDateTime(datasetRequest.audit[datasetRequest.audit.length - 1].at) }}</p>
                    </div>
                  </span>
                </div>
                <div v-if="!openAccessRequest" class="level-right">
                  <span class="level-item is-underlined"
                    >Show request form
                    <font-awesome-icon
                      icon="fa-solid fa-angle-down level-item"
                      class="is-size-3 ml-3"></font-awesome-icon
                  ></span>
                </div>
              </a>
            </div>
          </div>
        </div>
        <a v-if="openAccessRequest" class="level-right" @click="setOpenDatasetRequest(undefined, undefined)">
          <span class="level-item is-underlined">Close request form</span>
          <font-awesome-icon icon="fa-solid fa-close level-item" class="is-size-3"></font-awesome-icon>
        </a>
      </div>
    </div>

    <!-- Custodian and Admin View -->
    <div v-if="role === UserGroup.Administrators || role === UserGroup.DataCustodians">
      <div v-for="dataAccessRequest in computedDataAccessRequests" class="card mb-6" :key="dataAccessRequest.id">
        <header class="card-header has-text-black has-background-warning">
          <div
            class="card-header-button w-full card-header-icon py-3 my-4 px-6 has-text-left"
            aria-label="Show all request IDs">
            <table class="header-table">
              <th class="is-size-4 has-text-black">Data Access Request</th>
              <tr>
                <td class="header-property-column">Data Access Request ID:</td>
                <td class="header-data-column">{{ dataAccessRequest.id }}</td>
              </tr>
              <tr>
                <td class="header-property-column">Date Received:</td>
                <td class="header-data-column">
                  {{ convertToLocalDateTime(dataAccessRequest.datasetRequests[0].audit[0].at) }}
                </td>
              </tr>
              <tr>
                <td class="header-property-column">Requestor Organisation:</td>
                <td class="header-data-column">{{ dataAccessRequest.requestor.organisationName }}</td>
              </tr>
              <tr>
                <td class="header-property-column">Data Requestor:</td>
                <td class="header-data-column">
                  {{ dataAccessRequest.requestor.givenName }} {{ dataAccessRequest.requestor.familyName }}
                </td>
              </tr>
              <tr>
                <td class="header-property-column">Project Title:</td>
                <td class="header-data-column">{{ dataAccessRequest.project.title }}</td>
              </tr>
              <tr class="field" v-if="role === UserGroup.Administrators">
                <td class="header-property-column pt-2 has-text-weight-bold">DOI:</td>
                <td class="header-data-column">
                  <span class="is-flex is-align-items-center">
                    <div class="mt-2 mr-4 doi-input">
                      <o-input
                        :disabled="!dataAccessRequest.isDOIEditable"
                        v-model="dataAccessRequest.doi"
                        :class="
                          dataAccessRequest.isDOIEditable &&
                          dataAccessRequestDOIValidate(dataAccessRequest.doi).dataAccessRequestDOIClasses
                        "></o-input>
                    </div>
                    <font-awesome-icon
                      icon="fa-solid fa-pencil"
                      class="is-size-4 pt-3 pr-4 edit-icon"
                      @click="toggleEditDOI(dataAccessRequest)" />
                    <o-button
                      icon-pack="fas"
                      class="mt-2 is-success"
                      :class="{ 'is-loading': this.isLoading }"
                      :disabled="
                        !dataAccessRequestDOIValidate(dataAccessRequest.doi).valid ||
                        !dataAccessRequest.isDOIEditable ||
                        this.isLoading
                      "
                      @click="editDOI(dataAccessRequest.id, dataAccessRequest.doi)"
                      >Save</o-button
                    >
                  </span>
                </td>
              </tr>
              <tr class="field" v-if="role === UserGroup.DataCustodians">
                <td class="has-text-weight-bold">DOI:</td>
                <td>
                  <div class="mt-2 mr-4 doi-input">
                    <o-input :disabled="true" v-model="dataAccessRequest.doi"></o-input>
                  </div>
                </td>
              </tr>
            </table>
            <div class="parent-status">
              <p class="has-text-weight-bold is-size-5 is-inline-block mt-6">Data Access Request Status:</p>
              <p class="is-size-5">
                {{ !!dataAccessRequest.completed_at ? 'Complete' : 'Pending' }}
              </p>
              <div class="audit-data" v-if="!!dataAccessRequest.completed_at">
                <p class="has-text-weight-bold">Completed at:</p>
                <p>
                  {{ convertToLocalDateTime(dataAccessRequest.completed_at) }}
                </p>
              </div>
              <div class="pt-4" :class="{ 'pt-6': !dataAccessRequest.completed_at }">
                <div class="pt-6 mt-6 level-right">
                  <div v-if="openCollapsibles[dataAccessRequest.id]" class="b-noticeslevel-right">
                    <span class="level-item mt-4 is-underlined" @click="toggleCollapsible(dataAccessRequest.id)"
                      >Hide datasets included in this request<font-awesome-icon
                        icon="fa-solid fa-close level-item"
                        class="is-size-3 ml-3"></font-awesome-icon
                    ></span>
                  </div>
                  <div
                    v-if="!openCollapsibles[dataAccessRequest.id]"
                    :class="{ 'pt-4': !dataAccessRequest.completed_at }">
                    <span class="level-item is-underlined" @click="toggleCollapsible(dataAccessRequest.id)"
                      >Show datasets included in this request
                      <font-awesome-icon
                        icon="fa-solid fa-angle-down level-item"
                        class="is-size-3 ml-3"></font-awesome-icon
                    ></span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </header>
        <div
          class="card-content has-background-warning-light"
          :class="{ active: openCollapsibles[dataAccessRequest.id] }"
          :data-collapsible-content="dataAccessRequest.id">
          <h4 class="is-size-4 has-text-weight-bold py-2 pl-6 ml-5 has-text-black">
            Status of datasets included in request ({{ getFilteredDatasetRequests(dataAccessRequest).length }})
          </h4>
          <div
            v-for="datasetRequest in getFilteredDatasetRequests(dataAccessRequest)"
            :key="datasetRequest.id"
            class="dataset-card py-4">
            <a @click="setOpenDatasetRequest(dataAccessRequest.id, datasetRequest.id)">
              <div class="card-button py-4 px-5">
                <table>
                  <tr>
                    <td class="child-property-column">Dataset Request ID:</td>
                    <td class="child-data-column">{{ datasetRequest.id }}</td>
                  </tr>
                  <tr>
                    <td class="child-property-column">Date Received:</td>
                    <td class="child-data-column">
                      {{
                        datasetRequest.audit[0].at.substring(
                          0,
                          dataAccessRequest.datasetRequests[0].audit[0].at.indexOf('T')
                        )
                      }}
                    </td>
                  </tr>
                  <tr>
                    <td class="child-property-column">Dataset Title:</td>
                    <td class="child-data-column">{{ datasetRequest.metadataTitle }}</td>
                  </tr>
                  <tr>
                    <td class="child-property-column">Data Custodian:</td>
                    <td class="child-data-column">{{ datasetRequest.custodianName }}</td>
                  </tr>
                  <tr>
                    <td class="child-property-column">Data Custodian Email:</td>
                    <td class="child-data-column">{{ datasetRequest.custodianEmail }}</td>
                  </tr>
                  <tr
                    v-if="
                      datasetRequest.status !== 'Complete' &&
                      datasetRequest.status !== 'Declined' &&
                      role === UserGroup.DataCustodians
                    ">
                    <td class="child-property-column pt-5">Action:</td>
                    <td class="child-data-column pt-5">
                      <o-button
                        v-if="datasetRequest.status === 'New'"
                        variant="primary"
                        :class="isLoading ? 'is-loading' : ''"
                        :disabled="isLoading"
                        @click="(e: MouseEvent) => actionRequest(e, dataAccessRequest.id, datasetRequest.id, DatasetAction.Acknowledge)">
                        Acknowledge
                      </o-button>
                      <o-button
                        v-if="datasetRequest.status === 'Acknowledged'"
                        variant="success"
                        :class="isLoading ? 'is-loading' : ''"
                        :disabled="isLoading"
                        @click="(e: MouseEvent) => actionRequest(e, dataAccessRequest.id, datasetRequest.id, DatasetAction.Approve)">
                        Approve
                      </o-button>
                      <o-button
                        v-if="datasetRequest.status === 'Acknowledged'"
                        variant="danger"
                        class="ml-2"
                        :class="isLoading ? 'is-loading' : ''"
                        :disabled="isLoading"
                        @click="(e: MouseEvent) => actionRequest(e, dataAccessRequest.id, datasetRequest.id, DatasetAction.Decline)">
                        Decline
                      </o-button>
                      <o-button
                        v-if="datasetRequest.status === 'Approved'"
                        variant="info"
                        :class="isLoading ? 'is-loading' : ''"
                        :disabled="isLoading"
                        @click="(e: MouseEvent) => actionRequest(e, dataAccessRequest.id, datasetRequest.id, DatasetAction.AgreementSent)">
                        Send data agreement
                      </o-button>
                      <div v-if="datasetRequest.status === 'Data Agreement Sent'">
                        <o-button
                          :disabled="!datasetRequest.legalAgreementSigned || isLoading"
                          :class="isLoading ? 'is-loading' : ''"
                          variant="success"
                          @click="(e: MouseEvent) => actionRequest(e, dataAccessRequest.id, datasetRequest.id, DatasetAction.Complete)">
                          Complete
                        </o-button>
                        <o-checkbox
                          id="legal-agreement"
                          class="pt-3 ml-4"
                          v-model="datasetRequest.legalAgreementSigned">
                          Legal agreement signed
                        </o-checkbox>
                      </div>
                    </td>
                  </tr>
                </table>
                <span class="pl-6 ml-6 pb-6">
                  <div class="is-inline-block mr-2 has-text-weight-bold is-size-5">Dataset Status:</div>
                  <div class="is-inline-block is-size-5">
                    {{ datasetRequest.status }}
                  </div>
                  <div class="audit-data">
                    <p class="has-text-weight-bold">Last action:</p>
                    <p>{{ datasetRequest.audit[datasetRequest.audit.length - 1].action }} by</p>
                    <p>{{ datasetRequest.audit[datasetRequest.audit.length - 1].by }}</p>
                    <p>at {{ convertToLocalDateTime(datasetRequest.audit[datasetRequest.audit.length - 1].at) }}</p>
                  </div>
                </span>
              </div>
              <div v-if="!openAccessRequest" class="level-right">
                <span class="level-item is-underlined"
                  >Show request form
                  <font-awesome-icon icon="fa-solid fa-angle-down level-item" class="is-size-3 ml-3"></font-awesome-icon
                ></span>
              </div>
            </a>
          </div>
        </div>
      </div>
      <div class="buttons pt-2 level-right" v-if="!openAccessRequest">
        <o-button icon-pack="fas" class="button" @click="page = page - 1" :disabled="page === 0">
          <font-awesome-icon icon="fa-solid fa-angle-left" />
        </o-button>
        <o-button icon-pack="fas" class="button" @click="page = page + 1" :disabled="final_page">
          <font-awesome-icon icon="fa-solid fa-angle-right" />
        </o-button>
      </div>
      <a v-if="openAccessRequest" class="level-right" @click="setOpenDatasetRequest(undefined, undefined)">
        <span class="level-item is-underlined">Close request form</span>
        <font-awesome-icon icon="fa-solid fa-close level-item" class="is-size-3"></font-awesome-icon>
      </a>
    </div>
  </div>

  <DataAccessRequest
    v-if="openAccessRequest"
    ref="darForm"
    :read-only-fields="openAccessRequest"
    :access-values="[openAccessRequest.data.access]"
    :industryClassification-values="[openAccessRequest.project.industry]"
    :purpose-values="[openAccessRequest.project.purpose]"
    :researchClassification-values="[openAccessRequest.project.research]"
    @back="setOpenDatasetRequest(undefined, undefined)" />
</template>

<script lang="ts">
import { storeToRefs } from 'pinia';

import {
  actionRequestAPI,
  getAccessRequestsAPI,
  editDataAccessRequestDOIAPI,
  getAccessRequestsSearchAPI,
} from '@/api/api';
import PageHeadingWithDescription from '../components/PageHeadingWithDescription.vue';
import { type DataAccessRequestRead, DatasetAction, UserGroup } from '@/api/api.types';
import { defineComponent, type PropType } from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import DataAccessRequest from '@/views/DataAccessRequest.vue';
import dataAccessRequest from './DataAccessRequest.vue';
import { useUserDataStore, type UserData } from '@/store';
import { dataAccessRequestDOIValidator } from '@/helpers/helpers';
import { useProgrammatic } from '@oruga-ui/oruga-next';

interface DataAccessRequestActionState {
  userData: UserData;
  openCollapsibles: Record<string, boolean>;
  dataAccessRequests: DataAccessRequestRead[] | [];
  openAccessRequestId: string | undefined;
  openDatasetRequestId: string | undefined;
  isDOIEditable: boolean;
  notification: [string, boolean] | [] | null;
  idFilter: string | undefined;
  limit: number;
  currentCursor: string | undefined;
  previousCursors: string[] | undefined[];
  page: number;
  finalPageHit: boolean;
  isLoading: boolean;
}

export default defineComponent({
  components: {
    DataAccessRequest,
    PageHeadingWithDescription,
    FontAwesomeIcon,
  },
  props: {
    role: {
      type: String as PropType<UserGroup.DataCustodians | UserGroup.DataRequestors | UserGroup.Administrators>,
    },
  },
  data(): DataAccessRequestActionState {
    return {
      userData: storeToRefs(useUserDataStore()),
      openCollapsibles: {},
      dataAccessRequests: [] as DataAccessRequestRead[],
      openAccessRequestId: undefined as string | undefined,
      openDatasetRequestId: undefined as string | undefined,
      isDOIEditable: false,
      notification: null,
      idFilter: undefined,
      limit: 10,
      currentCursor: undefined,
      previousCursors: [],
      page: 0,
      finalPageHit: false,
      isLoading: false,
    };
  },
  async mounted() {
    this.getAccessRequests();
  },
  watch: {
    page(newPage, oldPage) {
      if (newPage > oldPage) {
        if (!this.finalPageHit || !this.previousCursors.includes(this.currentCursor)) {
          this.previousCursors.push(this.currentCursor);
        }
        this.getAccessRequests(this.currentCursor);
        if (this.final_page) {
          this.finalPageHit = true;
        }
      } else {
        this.getAccessRequests(this.previousCursors[newPage - 1]);
      }
    },
    limit() {
      this.previousCursors = [];
      this.currentCursor = undefined;
      this.page = 0;
      this.finalPageHit = false;
      this.getAccessRequests(this.currentCursor);
    },
  },
  methods: {
    toggleCollapsible(key: string) {
      this.openCollapsibles[key] = !this.openCollapsibles[key];

      if (this.openCollapsibles[key]) {
        this.$nextTick(() => {
          const collapsibleContent = document.querySelector(`[data-collapsible-content="${key}"]`);
          if (collapsibleContent) {
            collapsibleContent.scrollIntoView({
              behavior: 'smooth',
              block: 'center',
            });
            (collapsibleContent as HTMLElement).setAttribute('tabindex', '-1');
            (collapsibleContent as HTMLElement).focus();
            (collapsibleContent as HTMLElement).removeAttribute('tabindex');
          }
        });
      }
    },
    async getAccessRequests(cursor?: string | undefined) {
      const response = await getAccessRequestsAPI(this.role, this.limit, cursor);
      this.dataAccessRequests = response.data?.results || [];

      // Sort by date descending (most recent first)
      this.dataAccessRequests.sort((a, b) => {
        const dateA = new Date(a.datasetRequests[0]?.audit[0]?.at || 0).getTime();
        const dateB = new Date(b.datasetRequests[0]?.audit[0]?.at || 0).getTime();
        return dateB - dateA;
      });

      this.currentCursor = response.data?.cursor;
      this.idFilter = undefined;
    },
    async getAccessRequestsSearch() {
      if (this.idFilter !== '' && this.idFilter !== undefined) {
        const response = await getAccessRequestsSearchAPI(this.role, this.idFilter);
        // @ts-ignore
        this.dataAccessRequests = response.data ? [response.data.results] : [];
        this.currentCursor = response.data?.cursor;
      } else {
        this.getAccessRequests();
      }
    },
    setOpenDatasetRequest(accessRequestId: string | undefined, datasetRequestId: string | undefined) {
      this.openAccessRequestId = accessRequestId;
      this.openDatasetRequestId = datasetRequestId;

      if (accessRequestId && datasetRequestId) {
        this.$nextTick(() => {
          const darForm = this.$refs.darForm as any;
          if (darForm && darForm.$el) {
            darForm.$el.scrollIntoView({
              behavior: 'smooth',
              block: 'center',
            });
            darForm.$el.setAttribute('tabindex', '-1');
            darForm.$el.focus();
            darForm.$el.removeAttribute('tabindex');
          }
        });
      }
    },
    getFilteredDatasetRequests(dataAccessRequest: DataAccessRequestRead) {
      return this.openDatasetRequest ? [this.openDatasetRequest] : dataAccessRequest.datasetRequests;
    },
    async actionRequest(e: MouseEvent, accessRequestId: string, datasetRequestId: string, action: DatasetAction) {
      e.stopPropagation();
      this.isLoading = true;
      const { error } = await actionRequestAPI(accessRequestId, datasetRequestId, action);
      if (!error) {
        await this.getAccessRequests(this.previousCursors[this.page - 1]);
      }
      this.isLoading = false;
    },
    goBack() {
      if (!!this.openAccessRequestId || !!this.openDatasetRequest) {
        this.openAccessRequestId = undefined;
        this.openDatasetRequestId = undefined;
      } else {
        this.$router.push('/tools');
      }
    },
    dataAccessRequestDOIValidate(dataAccessRequestDOI: string) {
      return dataAccessRequestDOIValidator(dataAccessRequestDOI);
    },
    convertToLocalDateTime(timestamp: string) {
      const localDate = new Date(timestamp).toLocaleString('en-AU', {
        localeMatcher: 'best fit',
        timeZoneName: 'short',
      });
      return localDate;
    },
    toggleEditDOI(dataAccessRequest: DataAccessRequestRead) {
      dataAccessRequest.isDOIEditable = !dataAccessRequest.isDOIEditable;
    },
    async editDOI(dataAccessRequestId: string, dataAccessRequestDOI: Promise<string>) {
      const { oruga } = useProgrammatic();
      this.isLoading = true;
      this.notification = await editDataAccessRequestDOIAPI(dataAccessRequestId, dataAccessRequestDOI);
      this.isLoading = false;
      if (oruga.notification) {
        oruga.notification.open({
          variant: this.notification[1] ? 'success' : 'danger',
          message: this.notification[0],
          position: 'top',
          closable: true,
          duration: 5000,
        });
      }
    },
    searchById() {
      this.getAccessRequestsSearch();
    },
    clearFilter() {
      this.idFilter = undefined;
      this.getAccessRequests();
    },
  },
  computed: {
    UserGroup() {
      return UserGroup;
    },
    dataAccessRequest() {
      return dataAccessRequest;
    },
    DatasetAction() {
      return DatasetAction;
    },
    isLoggedIn() {
      return !!this.userData;
    },
    computedDataAccessRequests() {
      // If there's an open request, show that card above the request form
      return this.openAccessRequest ? [this.openAccessRequest] : this.dataAccessRequests;
    },
    openAccessRequest() {
      return this.openAccessRequestId
        ? this.dataAccessRequests.find((request) => request.id === this.openAccessRequestId)
        : undefined;
    },
    openDatasetRequest: function () {
      return this.openAccessRequest && this.openDatasetRequestId
        ? this.openAccessRequest.datasetRequests.find((request) => request.id === this.openDatasetRequestId)
        : undefined;
    },
    final_page() {
      return !this.currentCursor;
    },
  },
});
</script>

<style lang="scss" scoped>
.card-header-button {
  display: grid;
  grid-template-columns: 55% 2fr min-content;
  transition: 0.6s;
  color: black;
}

.card-button {
  display: grid;
  grid-template-columns: 55% 2fr min-content;
  transition: 0.6s;
  color: black;
}

.card-content:not(.active) {
  height: 0;
  padding-top: 0;
  padding-bottom: 0;
}
.card-content {
  padding-top: 2rem;
  overflow: hidden;
}
.dataset-card {
  padding-left: 3rem;
  padding-right: 3rem;
}

.header-table {
  border-collapse: separate;
  border-spacing: 0.5rem;
  line-height: 2;
}

.header-data-column {
  width: 20rem;
}

.header-property-column {
  min-width: 15rem;
  font-weight: bold;
}

.child-property-column {
  min-width: 16rem;
  font-weight: bold;
}

.child-data-column {
  min-width: 20rem;
  max-width: 30rem;
}

.doi-input {
  min-width: 30rem;
}

.audit-data {
  position: relative;
  top: 2rem;
}

.edit-icon {
  z-index: 100;
  color: #073d6e;
  &:hover {
    color: #0056b1;
  }
}

.input {
  width: 30rem;
}

.parent-status {
  padding-right: 2rem;
  text-align: right;
}
</style>
