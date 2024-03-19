<template>
  <div class="main">
    <div class="filter-zone row">
      <div class="col">
        <paginator
            :count="count"
            :per_page_def="per_page_def"
            @page_changed="page_changed"/>
      </div>
    </div>
    <table class="table">

    </table>
  </div>
</template>

<script>
import Paginated from "@/lib/mixins/Paginated";
import Paginator from "@/components/Paginator.vue";

export default {
  name: "Main",
  components: {Paginator},
  mixins: [Paginated],
  data() {
    return {}
  },
  methods: {}
}
</script>

<style scoped lang="scss">

</style>