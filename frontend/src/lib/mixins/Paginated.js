export default {
  data() {
    return {
      count: 1,
      per_page: 15,
      page: 1,

      per_page_def: 15,
    }
  },
  methods: {
    on_page_changed() {
      this.refresh()
    },
    page_changed(page, per_page = 15) {
      this.page = page
      this.per_page = per_page
      this.on_page_changed()
    }
  }
}
