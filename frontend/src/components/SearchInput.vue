<template>
  <input v-model="text"
         type="search"
         class="fc" placeholder="Поиск (Enter)"
         @keyup="searchTimeOut"
         @search.stop.prevent="searchTimeOut"
         @keyup.esc.prevent="clear" @keyup.enter="search"/>
</template>

<script>
export default {
  name: "SearchInput",
  data() {
    return {
      text: '',
      timeout: null,
    }
  },
  methods: {
    searchTimeOut() {
      clearTimeout(this.timeout)
      this.timeout = setTimeout(() => {
        this.search()
      }, 700);
    },

    search() {
      this.$emit('cr-search', this.text)
    },
    clear() {
      this.text = ''
      clearTimeout(this.timeout)
      this.timeout = setTimeout(() => {
        this.search()
      }, 300);
    },
  }
}
</script>

<style scoped>

</style>
