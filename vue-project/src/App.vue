<script setup>
import { ref, onMounted,watch} from "vue";
import axios from "axios";

const data = ref([]);
const headers = ref(["ID","NAME", "YEAR", "SELLING_PRICE", "KM_DRIVEN", "FUEL", "SELLER_TYPE", "TRANSMISSION", "OWNER"]);
const selectedValue = ref("");
const sortedData = ref([]);
const loading = ref(false);
const errorMessage = ref("");
const title = ref("");
const Value = ref([]);
const filtervalue = ref("");
const showSecondDropdown = ref(false); 

const fetchData = async () => { 
  try {
    const response = await axios.get("http://127.0.0.1:8000/cars/");
    if (Array.isArray(response.data)) {
      data.value = response.data;
      sortedData.value = [...data.value]; 
    } else {
      console.error("Unexpected data format:", response.data);
    }
  } catch (error) {
    console.error("Error fetching data:", error);
    errorMessage.value = "Failed to load data. Please try again.";
  }
};

const filter = async () => {
  if(!filtervalue.value){
    return;
  }
  try{
    const res = await axios.get(`http://127.0.0.1:8000/cars/filtercar/?${title.value.toLowerCase()}=${filtervalue.value}`);
    sortedData.value= res.data;
  }
  catch(err)
  {
    console.log(err);
  }
};

const groupBy = async () => {
      if (!selectedValue.value) {
        return;
      }

      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/cars/groupcars/${selectedValue.value.toLowerCase()}/`
        );

        if (response.data && Array.isArray(response.data.grouped_data)) {
          sortedData.value = response.data.grouped_data;
          console.log("Fetched Data:", sortedData.value);
        } else {
          console.error("Invalid response format:", response.data);
          sortedData.value = [];
        }
      } catch (error) {
        console.error("Error fetching grouped data:", error.response ? error.response.data : error.message);
        sortedData.value = [];
      }
    };

    watch(title, async (newTitle) => {
  if (newTitle) {
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/cars/distinct-values/${newTitle.toLowerCase()}/`
      );
      const data = await response.json(); 

      Value.value = [...data]; 
      showSecondDropdown.value = true;

      console.log("API Response:", data);
    } catch (error) {
      console.error("Error fetching data:", error);
      showSecondDropdown.value = false;
    }
  } else {
    showSecondDropdown.value = false;
  }
});


// Fetch data when component mounts
onMounted(fetchData);
</script>

<template>
  <div>
    <h1>CAR DETAILS TABLE</h1>

    <div class="controls">
      <div class="radio-group">
        <label v-for="(header, index) in headers" :key="index">
          <input type="radio" name="group" :value="header" v-model="selectedValue" />
          {{ header }}
        </label>
      </div>
      <button @click="groupBy" :disabled="loading">Group By</button>
    </div>
    <div>
      <select v-model="title">
        <option value="" disabled>Select an option</option>
        <option v-for="(header, index) in headers" :key="index">{{ header }}</option>
      </select>
      <select v-if="showSecondDropdown" v-model="filtervalue">
      <option value="" disabled>Select a value</option>
      <option v-for="(value, index) in Value" :key="index" :value="value">
        {{ value }}
      </option>
    </select>
      <button @click="filter" :disabled="loading">Filter Data</button>
    </div>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

    <table v-if="sortedData.length" border="2">
      <thead>
        <tr>
          <th v-for="(header, index) in headers" :key="index">
            {{ header }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, index) in sortedData" :key="index">
          <td v-for="(value, keyIndex) in Object.values(row)" :key="keyIndex">
            {{ value }}
          </td>
        </tr>
      </tbody>

    </table>

    
    <p v-if="!sortedData.length && !loading && !errorMessage">No data available.</p>
  </div>
</template>

<style scoped>
body {
  margin: 0;
  padding: 0;
  font-family: "Arial", sans-serif;
}

h1 {
  text-align: center;
  color: #f53152;
  font-weight: bold;
  margin: 10px 0;
}

.controls {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 10px;
}

.radio-group {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

button {
  padding: 10px;
  font-size: 17px;
  font-weight: bold;
  cursor: pointer;
  background-color: #f53152;
  color: white;
  border: none;
  border-radius: 5px;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

table {
  border-collapse: collapse;
  width: 100%;
  margin: 20px auto;
  color: black;
}

thead tr th {
  font-weight: bold;
  text-align: center;
  background-color: #d4cfd0;
}

th, td {
  padding: 10px;
  text-align: left;
}

.error {
  color: red;
  text-align: center;
}
</style>
