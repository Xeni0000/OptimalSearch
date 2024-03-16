<template>
  <div class="row m-0">
    <div class="col-2">
      <div class="row mb-2">
        <label>Путь до файла задач</label>
        <input v-model="form.path_to_tasks" class="fc">
      </div>
      <div class="row mb-2">
        <label>Путь до файла шаблонов</label>
        <input v-model="form.path_to_templates" class="fc">
      </div>
      <div class="row mb-2">
        <label>Путь до файла ролей</label>
        <input v-model="form.path_to_roles" class="fc">
      </div>
      <div class="row mb-2">
        <label>Путь до файла ролей списком</label>
        <input v-model="form.path_to_roles_list_wb" class="fc">
      </div>
      <div class="row">
        <button class="btn btn-primary"
                @click="write_to_db">
          Записать в бд
        </button>
      </div>
    </div>
    <div class="col-5">
      <template v-for="r in  not_added_roles">
        <div class="">
          {{ r }}
        </div>
      </template>
    </div>
    <div class="col-5">
      <template v-for="t in  not_added_tasks">
        <div class="">
          {{ t }}
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import Notify from "@/plugins/notify";

export default {
  name: "Main",
  data() {
    return {
      form: {
        path_to_tasks: 'C:\\Users\\Stas\\PycharmProjects\\OptimalSearch\\todo delete\\задачи.xlsx',
        path_to_templates: 'C:\\Users\\Stas\\PycharmProjects\\OptimalSearch\\todo delete\\Шаблоны.xlsx',
        path_to_roles: 'C:\\Users\\Stas\\PycharmProjects\\OptimalSearch\\todo delete\\Роли.xlsx',
        path_to_roles_list_wb: 'C:\\Users\\Stas\\PycharmProjects\\OptimalSearch\\todo delete\\роли список.xlsx',
      },

      not_added_roles: [],
      not_added_tasks: [],
    }
  },
  methods: {
    write_to_db() {
      this.$api.writer.write_on_db(this.form)
        .then(resp => {
          if (resp.success) {
            this.not_added_roles = resp.result.not_added_roles
            this.not_added_tasks = resp.result.not_added_tasks
          } else {
            Notify.error(resp.errors)
          }
        })
    }
  }
}
</script>

<style scoped lang="scss">

</style>