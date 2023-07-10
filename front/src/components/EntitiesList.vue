<template>
    <div class="entities">
      <h1>All Entities</h1>
      <div v-for="entity in entities" :key="entity.name" class="entity">
        <h2>{{ entity.name }}</h2>
        <p v-for="field in entity.fields" :key="field" class="field">
          {{ field }}
        </p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    name: 'EntitiesList',
    data () {
      return {
        entities: [],
      }
    },
    async created () {
      // Fetch the entities from the server when the component is created
      try {
        //const response = await axios.get('http://yourserver.com/api/entities')
        const response = await axios.get('assets/mocks/entities.json');
        this.entities = response.data
      } catch (error) {
        console.error('Failed to fetch entities:', error)
      }
    },
  }
  </script>
  
  <style scoped>
  .entities {
    padding: 20px;
  }
  
  .entity {
    margin-bottom: 20px;
  }
  
  .field {
    margin-left: 10px;
  }
  </style>
  