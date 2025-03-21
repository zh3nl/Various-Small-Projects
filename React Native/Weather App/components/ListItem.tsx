import { Feather } from "@expo/vector-icons";
import React from "react";
import { View, Text, StyleSheet } from "react-native";
import { weatherType } from "@/utilities/weatherType";
import moment from "moment";

const ListItem = (props: any) => {
  const { dt_txt, temp_min, temp_max, condition } = props;
  const { item, date, temp, dateTextWrapper} = styles;
  return (
    <View style={item}>
      <Feather name={weatherType[condition]?.icon} size={50} color={"white"} />
      <View style={dateTextWrapper}>
        <Text style={date}>{moment(dt_txt).format('dddd')}</Text>
        <Text style={date}>{moment(dt_txt).format('h:mm:ss a')}</Text>
      </View>
      <Text style={temp}>{`${Math.round(temp_min)}°/${Math.round(temp_max)}°`}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  item: {
    padding: 20,
    marginVertical: 8,
    marginHorizontal: 16,
    flexDirection: "row",
    justifyContent: "space-around",
    alignItems: "center",
    borderWidth: 5,
    backgroundColor: "indianred",
  },
  temp: {
    color: "white",
    fontSize: 20,
  },
  date: {
    color: "white",
    fontSize: 15,
  },
  dateTextWrapper: {
    flexDirection: "column"
  }
});

export default ListItem;
