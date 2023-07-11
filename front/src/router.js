import { createRouter, createWebHistory } from 'vue-router'
import EntitiesViewer from './components/EntitiesViewer.vue'
import ViewAll from './components/ViewAll.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: EntitiesViewer
  },
  {
    path: '/:entityName/all',
    name: 'ViewAll',
    component: ViewAll,
    props: true
  },
  // other routes...
]

const router = createRouter({
    history: createWebHistory(),
    routes
  });


export default router
