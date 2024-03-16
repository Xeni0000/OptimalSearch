import axios from "axios";

export default class WriterApi {
  static write_on_db(form) {
    return axios.post('/api/writer/write_on_db/', JSON.stringify(form))
  }
}