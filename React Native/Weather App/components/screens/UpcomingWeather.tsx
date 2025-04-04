import React from "react";
import {
  SafeAreaView,
  StyleSheet,
  FlatList,
  StatusBar,
  ImageBackground,
} from "react-native";
import { Feather } from "@expo/vector-icons";
import ListItem from "../ListItem";

const UpcomingWeather = ({weatherData}) => {
  const renderItem = ({ item }) => {
    return (
      <ListItem
        condition={item.weather[0].main}
        dt_txt={item.dt_txt}
        temp_min={item.main.temp_min}
        temp_max={item.main.temp_max}
      />
    );
  };

  const {container, image} = styles

  return (
    <SafeAreaView style={container}>
      <ImageBackground
        source={require("../../assets/images/upcoming-background.jpg")}
        style={image}
      >
        <FlatList
          data={weatherData}
          renderItem={renderItem}
          keyExtractor={(item) => item.dt_txt}
        ></FlatList>
      </ImageBackground>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    marginTop: StatusBar.currentHeight || 0,
    backgroundColor: "royalblue",
  },
  image: {
    flex: 1
  },
  title: {
    color: "white"
  }
});

export default UpcomingWeather;
