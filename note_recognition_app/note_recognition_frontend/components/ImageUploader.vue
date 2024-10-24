<template>
  <div class="uploader">
    <b-card class="mb-3" header="Upload an Image of a Currency Note" header-tag="header">
      <b-form @submit.prevent="uploadImage">
        <b-form-file v-model="image" accept="image/*"></b-form-file>
        <b-button type="submit" variant="dark" class="mt-3">Upload</b-button>
      </b-form>
      <div v-if="loading" class="mt-4 text-center">
        <b-spinner label="Loading..."></b-spinner>
        <p>Loading...</p>
      </div>
      <div v-if="!loading && prediction" class="mt-4">
        <h5>Denomination : {{ prediction }}</h5>
        <b-img :src="uploadedImageUrl" fluid alt="Uploaded Image"></b-img>
      </div>
    </b-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      image: null,
      prediction: null,
      uploadedImageUrl: null,
      loading: false,
    };
  },
  methods: {
    async uploadImage() {
      if (!this.image) {
        alert('Please select an image to upload.');
        return;
      }

      const formData = new FormData();
      formData.append('file', this.image);
      this.loading = true;

      try {
        const response = await this.$axios.post('https://note-recognition-app-ifbg.onrender.com/api/upload/', formData);
        this.prediction = response.data.data;
        this.uploadedImageUrl = URL.createObjectURL(this.image);
      } catch (error) {
        console.error('Error uploading image:', error);
        alert('Error uploading image. Please try again.');
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.uploader {
  max-width: 500px;
  margin: auto;
}
</style>
