<template>
    <div class="view-all">
      <h1 class="title">{{ entityName }}</h1>
      <button class="button create-button" @click="showCreateModal = true">Create</button>
      <div v-if="showCreateModal" class="modal">
        <div class="modal-content">
          <span class="close-button" @click="showCreateModal = false">&times;</span>
          <h2>Create New {{ entityName }}</h2>
          <div v-for="(value, key) in items[0]" :key="key" class="item-field">
            <label :for="key" class="field-key"><strong>{{ key }}: </strong></label>
            <input v-model="newItem[key]" :id="key" class="field-value" placeholder="Enter value" />
          </div>
          <button class="button update-button" @click="createItem()">Create</button>
        </div>
      </div>
      <div class="items-container">
        <div v-for="(item, index) in items" :key="index" class="item">
          <div v-for="(value, key) in item" :key="key" class="item-field">
            <p class="field-key"><strong>{{ key }}: </strong></p>
            <input v-model="item[key]" class="field-value" :placeholder="value" />
          </div>
          <div class="buttons">
            <button class="button update-button" @click="updateItem(item)">Update</button>
            <button class="button delete-button" @click="deleteItem(item)">Delete</button>
          </div>
        </div>
      </div>
    </div>
  </template>



  <script>
  export default {
    data() {
      return {
        entityName: '',
        items: [],
        newItem: {},
        showCreateModal: false,
      }
    },
    methods: {
        async createItem() {
            // PUT, POST or PATCH request to your API
            // You can reuse or adapt the updateItem() method code for this

            // Close the modal after successful creation
            this.showCreateModal = false;
            // Clear the newItem object
            this.newItem = {};
        },
        async updateItem(item) {
            try {
            const response = await fetch('/api/url', {
                method: 'PUT', // or 'POST'
                headers: {
                'Content-Type': 'application/json',
                },
                body: JSON.stringify(item),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log(data)

            // handle the response from your API
            } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
            }
        },
        deleteItem(item) {
            console.log(item)
        },
        // other methods...
    },
    async mounted() {
        try {
            const entityName = this.$route.params.entityName;
            this.entityName = entityName.charAt(0).toUpperCase() + entityName.slice(1); // to capitalize the first letter for display
            const data = await import(`@/assets/mocks/sql/${entityName.toLowerCase()}.json`); // Import the correct file based on the lowercased entityName
            this.items = data.default[entityName.toLowerCase()]; // Use the lowercase entityName
        } catch (e) {
            console.log('There was a problem with the import operation: ' + e.message);
        }
    }

}
</script>


<style scoped>

.modal {
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0,0,0,0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
  border-radius: 10px;
}

.close-button {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close-button:hover,
.close-button:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

.create-button, .update-button, .delete-button {
  margin: 10px;
  padding: 10px 20px;
  border-radius: 5px;
  border: none;
  font-size: 16px;
  transition: all 0.5s ease-in-out;
}

.create-button {
  background-color: #4CAF50;
  color: white;
}

.update-button {
  background-color: #008CBA;
  color: white;
}

.delete-button {
  background-color: #f44336;
  color: white;
}

.create-button:hover, .update-button:hover, .delete-button:hover {
  opacity: 0.8;
}

.field-value {
  display: block;
  width: 100%;
  padding: 10px 20px;
  margin: 10px 0;
  font-size: 18px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}
.view-all {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: Arial, sans-serif;
}

.title {
  color: #333;
  margin-bottom: 2rem;
}

.items-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2rem; /* Adds space between the items */
}

.item {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 10px; /* Gives rounded corners */
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* Adds a subtle shadow */
  width: 300px;
}

.item-field {
  margin-bottom: 0.5rem;
}

.field-key {
  font-weight: bold;
}

.field-value {
  color: #666;
}

.buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
}

.button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
}

.update-button {
  background-color: blue;
  color: white;
}

.delete-button {
  background-color: red;
  color: white;
}


.modal {
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0,0,0,0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
  border-radius: 10px;
}

.close-button {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close-button:hover,
.close-button:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

.create-button {
  background-color: green;
  color: white;
}
</style>