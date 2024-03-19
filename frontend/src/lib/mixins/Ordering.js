export default {
  data() {
    return {
      order_by: null,
      order_dir: null,
    }
  },
  methods: {
    on_ordering_change() {
      this.refresh()
    },
    order(field) {
      if (this.order_by == null) {
        this.order_by = field
        this.order_dir = '+'
      } else {
        if (this.order_by === field) {
          this.order_dir = this.order_dir === '+' ? '-' : '+'
        } else {
          this.order_by = field
          this.order_dir = '-'
        }
      }

      this.on_ordering_change()
    }
  }
}
