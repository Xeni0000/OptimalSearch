<template>
  <div class="top">
    <navbar-top/>
  </div>
  <div id="app" class="">
    <router-view/>
  </div>
</template>

<script>

import {defineComponent} from "vue";
import NavbarTop from "@/components/NavbarTop.vue";

export default defineComponent({
  components: {NavbarTop}
})
</script>

<style scoped lang="scss">

</style>
