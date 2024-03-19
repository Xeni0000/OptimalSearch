import Main from "@/views/Main.vue";
import WriteDB from "@/views/WriteDB.vue";
import FindingDependencies from "@/views/FindingDependencies.vue";

const routes = [
  {
    path: '/',
    name: 'main',
    component: Main
  },
  {
    path: '/write_db',
    name: 'write_db',
    component: WriteDB
  },
  {
    path: '/finding_dependencies',
    name: 'finding_dependencies',
    component: FindingDependencies
  },
]

export default routes