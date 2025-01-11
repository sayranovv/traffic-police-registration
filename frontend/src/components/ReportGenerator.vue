<script setup>
import {ref, onMounted, onUnmounted, computed} from 'vue'
import axios from 'axios'

import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'

const owners = ref([])
const yearLimit = ref(null)
const isLoading = ref(null)
const numOfReport = ref(null)

const screenWidth = ref(window.innerWidth)

const fetchOwners = async () => {
  isLoading.value = true
  try {
    const response = await axios.get('http://127.0.0.1:5000/owners');
    owners.value = response.data;
    console.log('yup', owners)
  } catch (error) {
    console.error('Ошибка при получении данных', error);
  } finally {
    isLoading.value = false
  }
}
const generateReport = async (reportType) => {
  numOfReport.value = reportType
  isLoading.value = true
  try {
    const payload = reportType === 3 ? { year_limit: yearLimit.value } : {};
    const response = await axios.post(`http://127.0.0.1:5000/reports/${reportType}`, payload);

    owners.value = response.data;
    console.log('yup')

  } catch (error) {
    console.error('Ошибка при создании отчёта', error);
  } finally {
    isLoading.value = false
  }
}

const updateScreenSize = () => {
  screenWidth.value = window.innerWidth
  console.log(screenWidth.value)
}

onMounted(() => {
  window.addEventListener('resize', updateScreenSize)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateScreenSize)
})

const isCorrectYear = computed(() => {
  return yearLimit.value >= 1950 && yearLimit.value <= 2025;
})

</script>

<template>
  <div class="p-8 rounded-3xl bg-blue-500 mx-auto my-auto flex flex-col justify-center items-center gap-6 text-white max-w-4xl" v-if="screenWidth > 640">
    <h1 class="text-4xl font-bold">Учёт в ГИБДД</h1>
    <div class="flex flex-wrap justify-center items-center gap-3">
      <button @click="fetchOwners" class="py-2 px-3 bg-blue-600 rounded-lg hover:bg-white hover:text-blue-600 transition-colors font-medium">Получить полный список</button>
      <button @click="generateReport(1)" class="py-2 px-3 bg-blue-600 rounded-lg hover:bg-white hover:text-blue-600 transition-colors font-medium">Отчёт 1</button>
      <button @click="generateReport(2)" class="py-2 px-3 bg-blue-600 rounded-lg hover:bg-white hover:text-blue-600 transition-colors font-medium">Отчёт 2</button>
      <div>
        <input v-model="yearLimit" placeholder="Год для отчёта 3" type="number" class="py-2 px-3 bg-blue-600 rounded-lg w-36 hover:bg-white hover:text-blue-600 transition-colors font-medium outline-none" />
        <button @click="generateReport(3)" :disabled="!isCorrectYear" class="ml-3 py-2 px-3 bg-blue-600 rounded-lg hover:bg-white hover:text-blue-600 transition-colors font-medium disabled:bg-gray-200 disabled:text-gray-300 disabled:bg-opacity-10">Отчёт 3</button>
      </div>
    </div>
    <div class="text-center">
      <div v-if="owners.length">
        <h2 v-if="!numOfReport" class="text-2xl font-semibold">Полный список</h2>
        <h2 v-else class="text-2xl font-semibold">Отчёт №{{ numOfReport }}</h2>
      </div>
      <div v-if="isLoading">Загрузка...</div>
    </div>
    <div class="px-2 max-w-2xl">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>ФИО</TableHead>
            <TableHead>Марка авто</TableHead>
            <TableHead>Рег. номер</TableHead>
            <TableHead>Мощность двигателя</TableHead>
            <TableHead>Год выпуска</TableHead>
            <TableHead>Год регистрации</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody v-if="owners.length && !isLoading" class="transition-all">
          <TableRow v-for="owner in owners" :key="owner.reg_number">
            <TableCell>
              {{ owner.surname }} {{ owner.name }} {{ owner.patronymic }}
            </TableCell>
            <TableCell>{{ owner.car_brand }}</TableCell>
            <TableCell>{{ owner.reg_number }}</TableCell>
            <TableCell>{{ owner.engine_volume }}</TableCell>
            <TableCell>{{ owner.year_of_release }}</TableCell>
            <TableCell>{{ owner.year_of_registration }}</TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </div>
  </div>
  <div v-else>
    <h1 class="text-3xl font-bold">Перверните экран!</h1>
  </div>
</template>

<style scoped>
</style>