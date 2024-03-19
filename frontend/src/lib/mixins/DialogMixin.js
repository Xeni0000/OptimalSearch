export default {
  data() {
    return {
      show_dialog: false,
      editing: false
    }
  },
  methods: {
    on_show() {

    },
    show() {
      this.on_show()
      this.show_dialog = true
    },
    on_edit_mode(obj){
    },
    edit_mode(data){
      this.on_edit_mode(data)
      this.editing = true
    },
    hide() {
      this.show_dialog = false
    },
    reset() {
      Object.assign(this.$data, this.$options.data.apply(this))
    }
  }
}
