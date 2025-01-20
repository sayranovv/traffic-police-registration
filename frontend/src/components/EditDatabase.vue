<script setup>
import {ref, onMounted, onUnmounted, computed} from 'vue'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import axios from 'axios'

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'

const owner = ref({
  surname: '',
      name: '',
      patronymic: '',
      reg_number: '',
      car_brand: '',
      engine_volume: '',
      year_of_release: '',
      year_of_registration: ''
})

const owners = ref([])
const deleteRegNumber = ref('')
const isLoading = ref(null)
const numOfReport = ref(null)
const alertText = ref('')

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

const updateScreenSize = () => {
  screenWidth.value = window.innerWidth
  console.log(screenWidth.value)
}

const addOwner = async () => {
  try {
    await axios.post('http://localhost:5000/owners', owner.value)
    showAlert('Владелец авто успешно добавлен в базу данных')
  } catch (error) {
    alert('Ошибка при добавлении владельца');
    console.error(error);
  }
}
const editOwner = async () => {
  try {
    const response = await axios.put(`http://localhost:5000/owners/${owner.value.reg_number}`, owner.value);
    showAlert('Данные владельца обновлены')
  } catch (error) {
    alert('Ошибка при редактировании владельца');
    console.error(error);
  }
}
const deleteOwner = async () => {
  try {
    const response = await axios.delete(`http://localhost:5000/owners/${deleteRegNumber.value}`);
    showAlert('Владелец авто успешно удален')
  } catch (error) {
    alert('Ошибка при удалении владельца');
    console.error(error);
  }
}

const showAlert = (message) => {
  alertText.value = message;
  console.log(alertText.value)
  setTimeout(() => {
    alertText.value = '';
  }, 2000)
}

onMounted(() => {
  window.addEventListener('resize', updateScreenSize)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateScreenSize)
})

</script>

<template>
  <div v-auto-animate v-if="alertText!==''" class="fixed top-0 left-0 w-full h-full z-10 bg-black bg-opacity-50">
    <Alert class="mx-auto top-1/3 w-1/3 drop-shadow-2xl">
      <AlertTitle>Успешно!</AlertTitle>
      <AlertDescription>
        {{ alertText }}
      </AlertDescription>
    </Alert>
  </div>

  <div
      class="p-8 rounded-3xl bg-slate-500 mx-auto my-auto flex flex-col justify-center items-center gap-6 text-white max-w-4xl"
      v-if="screenWidth > 640">
    <div class="w-full flex items-center justify-center gap-10 pl-6">
      <RouterLink to="/" class="mt-1 hover:underline">На главную</RouterLink>
      <h1 class="text-4xl font-bold ml-10">Учёт в ГИБДД</h1>
      <RouterLink to="/edit" class="mt-1 hover:underline ml-6">Редактировать базу</RouterLink>
    </div>
    <div class="flex gap-5">
      <div class="flex items-center justify-center gap-2 flex-wrap w-1/2 rounded-xl border-2 border-white p-3">
        <h2 class="text-2xl font-semibold">Добавление</h2>
        <div class="flex gap-2">
          <input v-model="owner.surname" placeholder="Фамилия" class="mt-2 py-2 px-3 w-full bg-slate-600 rounded-lg hover:bg-white hover:text-slate-600 transition-colors font-medium outline-none" />
          <input v-model="owner.name" placeholder="Имя" class="mt-2 py-2 px-3 w-full bg-slate-600 rounded-lg hover:bg-white hover:text-slate-600 transition-colors font-medium outline-none" />
          <input v-model="owner.patronymic" placeholder="Отчество" class="mt-2 py-2 px-3 w-full bg-slate-600 rounded-lg hover:bg-white hover:text-slate-600 transition-colors font-medium outline-none" />
        </div>
        <input v-model="owner.car_brand" placeholder="Марка авто" class="py-2 px-3 w-full bg-slate-600 rounded-lg hover:bg-white hover:text-slate-600 transition-colors font-medium outline-none" />
        <input v-model="owner.reg_number" placeholder="Рег. номер" class="py-2 px-3 w-full bg-slate-600 rounded-lg hover:bg-white hover:text-slate-600 transition-colors font-medium outline-none" />
        <input v-model="owner.engine_volume" placeholder="Мощность двигателя" type="number" class="py-2 px-3 w-full bg-slate-600 rounded-lg hover:bg-white hover:text-slate-600 transition-colors font-medium outline-none" />
        <input v-model="owner.year_of_release" placeholder="Год выпуска" type="number" class="py-2 px-3 w-full bg-slate-600 rounded-lg hover:bg-white hover:text-slate-600 transition-colors font-medium outline-none" />
        <input v-model="owner.year_of_registration" placeholder="Год регистрации" type="number" class="py-2 px-3 w-full bg-slate-600 rounded-lg hover:bg-white hover:text-slate-600 transition-colors font-medium outline-none" />
        <button @click="addOwner" class="py-2 px-3 bg-slate-600 w-full rounded-lg hover:bg-white hover:text-slate-600 transition-colors font-medium mt-3">Добавить</button>
      </div>
      <div class="flex items-center justify-center gap-2 flex-wrap w-1/2 rounded-xl border-2 border-white p-3">
        <h2 class="text-2xl font-semibold">Изменение</h2>
        <input v-model="owner.reg_number" placeholder="Рег. номер" class="mt-2 py-2 px-3 w-full bg-slate-600 rounded-lg hover:bg-white hover:text-slate-600 transition-colors font-medium outline-none" />
        <div class="flex gap-2">
          <input v-model="owner.surname" placeholder="Фамилия" class=" py-2 px-3 w-full bg-slate-600 rounded-lg hover:bg-white hover:text-slate-600 transition-colors font-medium outline-none" />
          <input v-model="owner.name" placeholder="Имя" class=" py-2 px-3 w-full bg-slate-600 rounded-lg hover:bg-white hover:text-slate-600 transition-colors font-medium outline-none" />
          <input v-model="owner.patronymic" placeholder="Отчество" class=" py-2 px-3 w-full bg-slate-600 rounded-lg hover:bg-white hover:text-slate-600 transition-colors font-medium outline-none" />
        </div>
        <input v-model="owner.car_brand" placeholder="Марка авто" class="py-2 px-3 w-full bg-slate-600 rounded-lg hover:bg-white hover:text-slate-600 transition-colors font-medium outline-none" />
        <input v-model="owner.engine_volume" placeholder="Мощность двигателя" type="number" class="py-2 px-3 w-full bg-slate-600 rounded-lg hover:bg-white hover:text-slate-600 transition-colors font-medium outline-none" />
        <input v-model="owner.year_of_release" placeholder="Год выпуска" type="number" class="py-2 px-3 w-full bg-slate-600 rounded-lg hover:bg-white hover:text-slate-600 transition-colors font-medium outline-none" />
        <input v-model="owner.year_of_registration" placeholder="Год регистрации" type="number" class="py-2 px-3 w-full bg-slate-600 rounded-lg hover:bg-white hover:text-slate-600 transition-colors font-medium outline-none" />
        <button @click="editOwner" class="py-2 px-3 bg-slate-600 w-full rounded-lg hover:bg-white hover:text-slate-600 transition-colors font-medium mt-3">Изменить</button>
      </div>
    </div>
    <div class="flex gap-5 w-full">
      <div class="w-1/2 rounded-xl border-2 border-white p-3 flex gap-2 items-center">
        <h2 class="text-2xl font-semibold">Удаление</h2>
        <input v-model="deleteRegNumber" placeholder="Рег. номер" class="py-2 px-3 w-full bg-slate-600 rounded-lg hover:bg-white hover:text-slate-600 transition-colors font-medium outline-none" />
        <button @click="deleteOwner" class="py-2 px-3 bg-slate-600 w-full rounded-lg hover:bg-white hover:text-slate-600 transition-colors font-medium">Удалить</button>
      </div>
      <button @click="fetchOwners"
              class="w-1/2 py-2 px-3 bg-slate-600 rounded-lg hover:bg-white hover:text-slate-600 transition-colors font-medium">
        Получить полный список
      </button>
    </div>
    <div class="flex flex-wrap justify-center items-center gap-3">

    </div>
    <div class="text-center">
      <div v-if="owners.length">
        <h2 v-if="!numOfReport" class="text-2xl font-semibold">Полный список</h2>
        <h2 v-else class="text-2xl font-semibold">Отчёт №{{ numOfReport }}</h2>
      </div>
      <div v-if="isLoading">Загрузка...</div>
    </div>
    <div class="px-2">
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