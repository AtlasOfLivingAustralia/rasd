<template>
  <nav
    class="navbar is-fixed-top"
    role="navigation"
    aria-label="main navigation"
    :style="{ 'background-color': navColor }">
    <div class="navbar-brand" v-bind:class="{ 'has-background-primary': isOpen }">
      <RouterLink class="navbar-item px-5" to="/">
        <font-awesome-icon icon="fa-solid fa-house" />
      </RouterLink>
      <a
        role="button"
        class="navbar-burger has-text-white"
        aria-label="menu"
        aria-expanded="false"
        @click="isOpen = !isOpen"
        :class="{ 'is-active': isOpen }">
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </a>
    </div>
    <div class="navbar-menu is-filter pr-3" :class="{ 'is-active': isOpen, 'has-background-primary': isOpen }">
      <div class="navbar-end is-filter has-text-centered">
        <RouterLink class="navbar-item" :to="{ name: 'search' }"
          >Search <font-awesome-icon icon="fa-solid fa-magnifying-glass" class="pl-2"
        /></RouterLink>
        <div class="navbar-item has-dropdown is-hoverable" id="dropdown">
          <RouterLink class="navbar-link has-text-white" :to="{ name: 'about' }">About</RouterLink>
          <div class="navbar-dropdown" :style="{ 'background-color': navColor }">
            <RouterLink :to="{ name: 'privacy-notice' }" class="navbar-item" id="dropdown-link"
              >Privacy Notice</RouterLink
            >
            <RouterLink :to="{ name: 'terms-of-use' }" class="navbar-item" id="dropdown-link">Terms of Use</RouterLink>
            <a
              href="https://rasd.org.au/pdf/RASD-User-Guide.pdf"
              target="_blank"
              rel="noopener noreferrer"
              class="navbar-item"
              id="dropdown-link"
              >User Guide</a
            >
          </div>
        </div>
        <div v-if="userData.id">
          <div class="navbar-item has-dropdown is-hoverable" id="dropdown">
            <p class="navbar-link has-text-white" :style="{ 'background-color': navColor }">
              Welcome {{ userData.givenName }} {{ userData.familyName }} ({{ userGroupDisplay }})
            </p>
            <div class="navbar-dropdown" :style="{ 'background-color': navColor }">
              <RouterLink :to="{ name: 'tools' }" class="navbar-item" id="dropdown-link"> Tools </RouterLink>
              <RouterLink to="/" @click="logOut" class="navbar-item" id="dropdown-link"> Logout </RouterLink>
            </div>
          </div>
        </div>
        <div v-else class="level">
          <RouterLink class="navbar-item" :to="{ name: 'login' }">Login</RouterLink>
          <RouterLink class="navbar-item" :to="{ name: 'register' }">Register</RouterLink>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { storeToRefs } from 'pinia';
import { logOutAndClearUserData, useUserDataStore } from '@/store';

export default {
  name: 'NavigationBar',
  data() {
    return {
      isOpen: false,
      scrollPosition: [0, 0],
      userData: storeToRefs(useUserDataStore()),
    };
  },
  computed: {
    yPosition() {
      return this.scrollPosition[1];
    },
    navColor() {
      // drop to translucent based on y value
      // Static number, 22rem in pixels
      const heroHeight = 352;
      return `rgb(7, 61, 110, ${this.yPosition / heroHeight})`;
    },
    userGroupDisplay() {
      if (this.userData.groups && this.userData.groups.length > 0) {
        return this.userData.groups[0]
          .replace(/DataRequestors/g, 'Data Requestor')
          .replace(/DataCustodians/g, 'Data Custodian')
          .replace(/Administrators/g, 'Administrator');
      } else {
        return 'Unknown';
      }
    },
  },
  methods: {
    logOut() {
      logOutAndClearUserData();
      this.$router.push('/');
    },
  },
  beforeUnmount() {
    // Detach before unmounting
    window.removeEventListener('scroll', this.scrollListener);
  },
  async mounted() {
    // Scroll listener for updating the navbar background colour style
    this.scrollListener = () => {
      this.scrollPosition = [Math.round(window.pageXOffset), Math.round(window.pageYOffset)];
    };
    // Instantiate initial position
    this.scrollListener();
    window.addEventListener('scroll', this.scrollListener);
  },
};
</script>

<style scoped>
/* Dropdown arrow colour */
.navbar-link:not(.is-arrowless)::after {
  border-color: #f4faf4;
}
.navbar-item {
  color: #f4faf4;
  position: relative;
  text-decoration: none;
  padding-bottom: 8px;
}

.navbar-link:not(.is-arrowless)::after {
  border-color: #f4faf4;
  margin-top: -0.375em;
  right: 1.125em;
}

.navbar-dropdown {
  border-top: none;
}

.navbar-link {
  height: 3.5rem;
}
</style>
