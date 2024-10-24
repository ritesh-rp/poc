<!-- layouts/default.vue -->
<template>
  <div class="d-flex flex-column min-vh-100">
    <Header />
    <b-container class="flex-grow-1 my-5">
      <Nuxt />
    </b-container>
    <Footer />
  </div>
</template>

<script>
import Header from '~/components/Header.vue';
import Footer from '~/components/Footer.vue';

export default {
  components: {
    Header,
    Footer
  }
};
</script>

<style>
/* Ensure footer stays at the bottom */
.d-flex {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.flex-grow-1 {
  flex-grow: 1;
}
</style>
