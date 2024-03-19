import axios from "axios";

export default class FindingDependenciesApi {
  static find_tasks_duplicate_dependence(form) {
    return axios.post('/api/finding_dependencies/tasks/', JSON.stringify(form))
  }
}