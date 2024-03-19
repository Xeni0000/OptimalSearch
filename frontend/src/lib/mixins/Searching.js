export default {
  data() {
    return {
      search_text: ''
    }
  },
  methods: {
    search(text) {
      this.search_text = text
      this.refresh()
    }
  }
}
