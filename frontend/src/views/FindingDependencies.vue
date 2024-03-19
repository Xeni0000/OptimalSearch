<template>
  <div class="row m-0">
    <div class="col-2">
      <div class="row mb-2">
        <label>Путь до файла пользователя</label>
        <input v-model="form.path_to_user_templates" class="fc">
      </div>
      <div class="row">
        <button class="btn btn-primary w-100"
                @click="">
          Начать поиск
        </button>
      </div>
    </div>
    <div class="col-8">
      <div class="filter-zone row">
        <div class="col-3">
          <search-input/>
        </div>
      </div>
      <table class="table">
        <thead>
        <tr>
          <th>Название задачи</th>
          <th>Роли</th>
        </tr>
        </thead>
        <tbody>
        <template v-for="t in tasks">
          <tr class="">
            <td>
              {{ t.task.name }}
            </td>
            <td>
              <template v-for="r in t.roles">
                <div class="">
                  {{ r.name }}
                </div>
              </template>
            </td>
          </tr>
        </template>
        </tbody>
      </table>
    </div>
    <div class="col-2">
      <button class="btn btn-primary w-100"
              @click="find_tasks_duplicate_dependence">
        Найти повторяющиеся задачи
      </button>
    </div>
  </div>
</template>

<script>
import Paginator from "@/components/Paginator.vue";
import Paginated from "@/lib/mixins/Paginated";
import SearchInput from "@/components/SearchInput.vue";

export default {
  name: "FindingDependencies",
  components: {SearchInput, Paginator},
  mixins: [Paginated],
  data() {
    return {
      form: {
        path_to_user_templates: ''
      },

      tasks: []
    }
  },
  methods: {
    find_tasks_duplicate_dependence() {
      this.$api.fd.find_tasks_duplicate_dependence()
        .then(resp => {
          if (resp.success) {
            this.tasks = resp.result.tasks
            this.count = resp.result.count
          } else {

          }
        })
    }
  }
}
</script>

<style scoped lang="scss">

</style>