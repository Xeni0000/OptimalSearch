<template>
  <div class="navbar row">
    <div class="col t-c">
      <div class="btn btn-primary"
           @click="$router.push({name: 'main'})">
        Главная
      </div>
      <div class="btn btn-primary mx-4"
           @click="$router.push({name: 'write_db'})">
        Загрузка базы
      </div>
      <div class="btn btn-primary"
           @click="$router.push({name: 'finding_dependencies'})">
        Поиск зависимостей
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "NavbarTop"
}
</script>

<style scoped lang="scss">

</style>