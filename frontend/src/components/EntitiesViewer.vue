<template>
  <div class="entities">
    <div v-for="(entity, entityName) in entities" :key="entityName" class="entity" @click="toggleDetails(entityName)">
      <div class="entity-header">
        <img :src="getImage(entity.type)" class="entity-logo" alt="Entity Logo"/>
        <div>
          <h2 class="entity-name">{{ entityName }}</h2>
          <p v-if="entityDetailsShown[entityName]" class="entity-description">{{ entity.description }}</p>
        </div>
      </div>
      <ul v-if="entityDetailsShown[entityName]" class="entity-fields">
        <li v-for="(description, fieldName) in entity.fields" :key="fieldName">
          <h3 class="field-name">{{ fieldName }}</h3>
          <p class="field-description">{{ description }}</p>
        </li>
        <li class="view-all-container">
          <!-- Router Link Component for View All -->
          <router-link :to="`/${entityName}/all`">
            <button class="view-all-button">View All</button>
          </router-link>
        </li>
      </ul>
    </div>
  </div>
</template>


<script>
import entities from '@/assets/mocks/entities.json'

export default {
  data() {
    return {
      entities: entities,
      entityDetailsShown: {}  // This object will hold the visibility state of each entity details
    }
  },
  methods: {
    toggleDetails(entityName) {
      if (this.entityDetailsShown[entityName]) {
        this.entityDetailsShown[entityName] = !this.entityDetailsShown[entityName];
      } else {
        this.entityDetailsShown[entityName] = true;
      }
    },
    viewAllDetails(entityName) {
      this.$router.push({ name: 'ViewAll', params: { entityName: entityName } });
    },

    getImage(entityType) {
      return entityType === 'entity' ? require('@/assets/logos/entity.png') : require('@/assets/logos/relationship.png');
    }
  }
}

</script>

<style scoped>
.entities {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.entity {
  border: 1px solid #e1e8ed;
  border-radius: 10px;
  padding: 10px;
  background-color: white;
  cursor: pointer;
  transition: 0.3s all ease-in-out;
}

.entity:hover {
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19);
}

.title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 5px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.entity-header {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.description {
  font-size: 12px;
  color: #888;
  margin-bottom: 10px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.fields {
  list-style-type: none;
  padding-left: 0;
  margin-top: 10px;
}

.field-name {
  font-weight: bold;
  font-size: 14px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.field-description {
  margin-left: 10px;
  font-size: 12px;
  color: #666;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.entities {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.entity {
  display: flex;
  align-items: center;
  gap: 15px;
}

.entity-logo {
  border-radius: 50%;  /* This makes the image circular */
  width: 50px;  /* Adjust as needed */
  height: 50px;  /* Adjust as needed */
}

.view-all-button {
  border: none;
  background-color: #007BFF; /* Or any color you prefer */
  color: #FFF;
  padding: 10px 20px;
  border-radius: 50px; /* For rounded corners */
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.view-all-button:hover {
  background-color: #0056b3; /* Darker shade for hover */
}

.view-all-container {
  display: flex;
  justify-content: center; /* Center the button */
  margin-top: 10px;
}

</style>
