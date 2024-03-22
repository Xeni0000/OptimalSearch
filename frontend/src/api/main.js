import axios from "axios";

export default class MainApi {
  static role_list(page, per_page, search_text) {
    return axios.get('/api/main/role_list/', {
      params: {
        page, per_page, search_text
      }
    })
  }

  static task_list(page, per_page, search_text) {
    return axios.get('/api/main/task_list/', {
      params: {
        page, per_page, search_text
      }
    })
  }
}