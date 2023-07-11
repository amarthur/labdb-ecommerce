<template>
  <div id="app">
    <div class="navbar">
      <router-link to="/">
        <img src="@/assets/logo.png" alt="Logo" class="logo" />
      </router-link>
      <input type="text" placeholder="Search..." :class="['search', true ? 'search-logged-in' : 'search-logged-out']" />
    </div>

    <h1 class="title">Event Feed</h1>
    <div class="event-feed">
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  components: {},
  data() {
    return {}
  },
  methods: {
    toggleDropdown() {
      this.isDropdownShown = !this.isDropdownShown;
    },
  },
  computed: {
    sortedEvents() {
      return this.events.slice().sort((a, b) => a.date - b.date);
    }
  }
}
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  margin: 0 auto;
}

h1 {
  text-align: center;
}

.event-card {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.event-card img {
  width: 80%;
  height: auto;
  object-fit: cover;
  border-radius: 15px;
  max-height: 200px;
}

.event-card .date {
  font-size: 0.9rem;
  color: #6c757d;
  margin-bottom: 0.5rem;
}

.event-card .description {
  font-size: 1.1rem;
  color: #343a40;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.2em 1em;
  background-color: #f9f9f9;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: fixed;
  width: 100%;
  max-width: 97%;
  margin: auto;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.navbar-right {
  display: flex;
  gap: 1em;
  margin-right: 2em;
}
.logo {
  width: 70px;
  height: auto;
}

.search {
  margin: 0 1em;
  padding: 0.5em;
  border: none;
  border-radius: 4px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.search-logged-out {
  flex-grow: 1;
}

.search-logged-in {
  flex-grow: 0.95;
}

.buttons {
  display: flex;
  align-items: center;
  gap: 1em;
}

.btn {
  padding: 0.5em 1em;
  border: none;
  border-radius: 4px;
  background-color: #007bff;
  color: #fff;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn:hover {
  background-color: #0056b3;
}

.btn.login {
  background-color: #6c757d;
}

.btn.login:hover {
  background-color: #5a6268;
}
.btn.create-event {
  background-color: #54bb00;
}
body {
  padding-top: 50px;
}

.user-profile {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  margin-left: 10px;
}

.user-section {
  display: flex;
  align-items: center;
  gap: 1em;
}

.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f9f9f9;
  min-width: 120px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  padding: 12px 16px;
  z-index: 1;
  right: 0;
  top: 100%;
}

.dropdown-content button {
  background: none;
  color: black;
  padding: 0;
  margin: 0;
  border: none;
  text-decoration: none;
  width: 100%;
  text-align: left;
}

.dropdown:hover .dropdown-content {
  display: block;
}

</style>
