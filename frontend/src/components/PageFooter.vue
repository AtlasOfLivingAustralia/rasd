<template>
  <footer class="footer py-6">
    <div class="container pt-4">
      <div class="is-variable is-desktop">
        <h3 class="subtitle is-5 has-text-weight-bold has-text-left has-text-primary">CITING THE FRAMEWORK:</h3>
        <p class="has-text-justified has-text-primary pb-3">
          For bibliographic purposes this publication may be cited as: National Framework for the Sharing of Restricted
          Access Species Data in Australia 2023, Atlas of Living Australia, Publication Series No. 6, Canberra,
          Australia. https://doi.org/10.54102/ala.94894.
          <br />
          Supplements of this publications are regularly updated and may be cited as: National Framework for the Sharing
          of Restricted Access Species Data in Australia 2023, Supplement Recognising Indigenous Data Sovereignty
          1/12/2023, Atlas of Living Australia, CSIRO, Canberra. https://doi.org/10.54102/ala.94894.
        </p>
        <div class="py-2 mt-6 pt-6 has-text-centered">
          <a href="https://doi.org/10.54102/ala.94894">DOI: https://doi.org/10.54102/ala.94894</a>
          <RouterLink class="px-6" :to="{ name: 'privacy-notice' }">Privacy Notice</RouterLink>
          <RouterLink class="pr-6" :to="{ name: 'terms-of-use' }">Terms of Use</RouterLink>
          <span class="has-text-primary">v{{ version }}</span>
        </div>
      </div>
    </div>
  </footer>
  <div class="has-text-centered has-background-primary py-4">
    <img src="../assets/fullwidth_footer_graphic.png" alt="Footer image of native Australian animals" />
  </div>
</template>
<script setup>
// eslint-disable-next-line no-undef
const version = __APP_VERSION__; // this is a vite framework variable, not an application variable.
</script>
<style scoped>
footer {
  background-color: #c5e2ef;
}
</style>
