import { createApp } from 'vue';
import { createPinia } from 'pinia';
import piniaPluginPersistedState from 'pinia-plugin-persistedstate';
import App from './App.vue';
import router from './router';
import Oruga from '@oruga-ui/oruga-next';
import { bulmaConfig } from '@oruga-ui/theme-bulma';
import '@oruga-ui/theme-bulma/dist/bulma.css';
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import {
  faHouse,
  faMagnifyingGlass,
  faAngleLeft,
  faAngleRight,
  faAngleDown,
  faTimes,
  faLocationDot,
  faBook,
  faFileLines,
  faBuilding,
  faTag,
  faListCheck,
  faCirclePlus,
  faClipboardList,
  faRightLeft,
  faListUl,
  faQuestionCircle,
  faListAlt,
  faPeopleRoof,
  faPencil,
  faTrash,
} from '@fortawesome/free-solid-svg-icons';
import './assets/main.scss';

library.add(
  faHouse,
  faMagnifyingGlass,
  faAngleLeft,
  faAngleRight,
  faAngleDown,
  faTimes,
  faLocationDot,
  faBook,
  faFileLines,
  faBuilding,
  faTag,
  faListCheck,
  faCirclePlus,
  faClipboardList,
  faRightLeft,
  faListUl,
  faQuestionCircle,
  faListAlt,
  faPeopleRoof,
  faPencil,
  faTrash
);

const pinia = createPinia();
pinia.use(piniaPluginPersistedState);

createApp(App)
  .use(pinia)
  .use(Oruga, bulmaConfig)
  .use(router)
  .component('font-awesome-icon', FontAwesomeIcon)
  .mount('#app');
