<template>
  <div class="main">
    <div class="filter-zone row">
      <div class="col-2">
        <search-input @cr-search="search"/>
      </div>
      <div class="col-1">
        <select v-model="table_type" @change="refresh"
                class="form-control">
          <option value="0">Роли</option>
          <option value="1">Задачи</option>
        </select>
      </div>
      <div class="col">
        <paginator
            :count="count"
            :per_page_def="per_page_def"
            @page_changed="page_changed"/>
      </div>
    </div>
    <template v-if="table_type===0">
      <table class="table">
        <thead>
        <tr>
          <th>Название</th>
          <th>Сегмент</th>
          <th>Приложение</th>
          <th>Задачи</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="r in roles">
          <td>{{ r.name }}</td>
          <td>{{ r.attachment.segment.name }}</td>
          <td>{{ r.attachment.name }}</td>
          <td>
            <div v-for="t in r.tasks">
              {{ t.name }}
            </div>
            <div v-if="r.tasks.length === 0">
              Список пуст
            </div>
          </td>
        </tr>
        <tr v-if="roles.length === 0">
          <td colspan="4">Список пуст</td>
        </tr>
        </tbody>
      </table>
    </template>
    <template v-else>
      <table class="table">
        <thead>
        <tr>
          <th>Название</th>
          <th>Сегмент</th>
          <th>Приложение</th>
          <th>Задачи</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="r in tasks">
          <td>{{ r.name }}</td>
          <td>{{ r.folder.subsystem.name }}</td>
          <td>{{ r.folder.name }}</td>
          <td>
            <div v-for="t in r.roles">
              {{ t.name }}
            </div>
            <div v-if="r.roles.length === 0">
              Список пуст
            </div>
          </td>
        </tr>
        <tr v-if="tasks.length === 0">
          <td colspan="4">Список пуст</td>
        </tr>
        </tbody>
      </table>
    </template>
  </div>
</template>

<script>
import Paginated from "@/lib/mixins/Paginated";
import Paginator from "@/components/Paginator.vue";
import Notify from "@/plugins/notify";
import SearchInput from "@/components/SearchInput.vue";
import Searching from "@/lib/mixins/Searching";

export default {
  name: "Main",
  components: {SearchInput, Paginator},
  mixins: [Paginated, Searching],
  data() {
    return {
      table_type: 0,
      roles: [],
      tasks: [],
    }
  },
  mounted() {
    this.refresh()
  },
  methods: {
    refresh() {
      this.table_type === 0 ? this.role_list() : this.task_list()
    },
    role_list() {
      this.$api.main.role_list(this.page, this.per_page, this.search_text)
        .then(resp => {
          if (resp.success) {
            this.roles = resp.result.roles
            this.count = resp.result.count
          } else {
            Notify.error(resp.errors)
          }
        })
    },
    task_list() {
      this.$api.main.task_list(this.page, this.per_page, this.search_text)
        .then(resp => {
          if (resp.success) {
            this.tasks = resp.result.tasks
            this.count = resp.result.count
          } else {
            Notify.error(resp.errors)
          }
        })
    },
  }
}
</script>

<style scoped lang="scss">
.main {
  padding: 1rem;
}
</style>