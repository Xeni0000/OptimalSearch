<template>
  <div class="pagination-cr" v-show="pages>1">
    <div class="pag-per-page">
      <i class="bi bi-caret-up-fill btn-incr"
         @click="per_page_step('+')"></i>
      <i class="bi bi-caret-down-fill btn-decr"
         :class="{'min': per_page === 1}"
         @click="per_page_step('-')"></i>

      <input type="number" disabled :value="per_page">
    </div>
    <el-pagination v-model="page"
                   :page-size="per_page"
                   :total="count"
                   :pager-count="pager_count"
                   layout="pager"
                   @current-change="page_changed">
    </el-pagination>
  </div>
</template>

<script>

export default {
  name: "Paginator",
  props: ['per_page_def', 'count'],
  emits: ['page_changed'],
  data() {
    return {
      page: 1,
      step: 0,
      pager_count: 5,
    }
  },
  methods: {
    per_page_step(sign) {
      if (sign === '+') {
        this.step++
        this.$emit('page_changed', this.page, this.per_page)
      } else if (sign === '-' && this.per_page > 1) {
        this.step--
        this.$emit('page_changed', this.page, this.per_page)
      }
    },
    page_changed(page) {
      this.page = page
      this.$emit('page_changed', this.page, this.per_page)
    }
  },
  computed: {
    per_page() {
      let res = 0

      res = this.per_page_def

      res += this.step

      return res
    },

    pages() {
      let res = Math.ceil(this.count / this.per_page)
      return res ? res : 1
    },
  },
}
</script>

<style scoped lang="scss">
input[type=number]::-webkit-inner-spin-button,
input[type=number]::-webkit-outer-spin-button {
  -webkit-appearance: none;
}

div.pagination-cr {
  .pag-per-page {
    .btn-incr, .btn-decr {
      position: absolute;
      right: 4px;
      z-index: 1;
      font-size: 21px;

      &:not( .max, .min) {
        color: $color-white;
      }

      color: $color-border-gray;
    }

    .btn-incr {
      top: -6px;
    }

    .btn-decr {
      bottom: -6px;
    }

    input {
      width: 50px;
      border: $blue-hover 1px solid;
      border-left: 0;
      border-bottom-right-radius: 5px;
      border-top-right-radius: 5px;
      background-color: $color-background-dark;
      position: absolute;
      height: 100%;
      padding-left: 5px;
      right: 0;
    }
  }

  .el-pagination {
    margin-right: 38px;
    border: $blue-hover 1px solid;
    border-bottom-left-radius: 5px;
    border-top-left-radius: 5px;
    background-color: $color-background-dark;
  }

  width: auto;

  opacity: 0.5;
  position: absolute;
  top: 40px;
  right: 0;

  .el-pager {
    .number {
      color: $color-background-dark;
      border-radius: 0;
      padding: 20px 15px;
      font-size: 18px;

      &.is-active {
        background-color: $blue-hover;
      }
    }
  }

  &:hover {
    opacity: 1;

    .el-pager {
      .number {
        color: $text-dark;
      }
    }
  }

}
</style>
