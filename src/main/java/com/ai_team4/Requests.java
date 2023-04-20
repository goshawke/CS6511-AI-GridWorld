package com.ai_team4;

import okhttp3.*;
import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

public class Requests {

	final static String baseGwUrl = "https://www.notexponential.com/aip2pgaming/api/rl/gw.php";
	final static String baseScoreUrl = "https://www.notexponential.com/aip2pgaming/api/rl/score.php";
	final static String teamId = "1387";
	final static String userId = "1201";

	public static void main(String[] args) throws IOException {

		////////////////////////
		// GET method testing//
		////////////////////////

		// testing
		// get_location();

		// testing
		// get_learning_score();

		// testing
		// get_last_x_runs("1");

		// testing
		// reset();

		////////////////////////
		// POST method testing//
		////////////////////////

		// testing
		// enter_world("0");

		// testing
		// make_move("0", "N");

	} // main

	////////////////////
	// POST API CALLS //
	////////////////////

	/*
	 * enter_world(String worldId)
	 * 
	 * Result:
	 * {"code":"OK","worldId":#,"runId":###,"state":"#:#"}
	 * 
	 */
	static String enter_world(String worldId) throws IOException {
		OkHttpClient client = new OkHttpClient().newBuilder()
				.build();
		MediaType mediaType = MediaType.parse("application/x-www-form-urlencoded");
		RequestBody body = new MultipartBody.Builder().setType(MultipartBody.FORM)
				.addFormDataPart("type", "enter")
				.addFormDataPart("worldId", worldId)
				.addFormDataPart("teamId", teamId)
				.build();
		Request request = new Request.Builder()
				.url("https://www.notexponential.com/aip2pgaming/api/rl/gw.php")
				.method("POST", body)
				.addHeader("userId", userId)
				.addHeader("x-api-key", "05049c9e31fc51cdb173")
				.addHeader("Content-Type", "application/x-www-form-urlencoded")
				.build();
		Response response = client.newCall(request).execute();
		// System.out.println(response.body().string());

				// holds the response from the API call
		String jsonResponse = response.body().string();

		// Accessing the JSON values within the response string using the jsonNOde
		// object
		ObjectMapper objectMapper = new ObjectMapper();
		JsonNode jsonNode = objectMapper.readTree(jsonResponse);

		String code = jsonNode.get("code").asText();

		if (code.equals("FAIL")) {
			try {
				String message = jsonNode.get("message").asText();
				System.out.println("FAIL: enter_world(), Message: " + message);
			} catch (Exception e) {
				System.out.println("FAIL: enter_world()");
			}
			return "-1";
		} else if (code.equals("OK")) {
			System.out.println("TeamId " + teamId + " successfully entered World " + worldId);
			return "1";
		} else {
			System.out.println("Unknown Error: enter_world()");
			return "-1";
		}
	} // enter_world()

	/*
	 * make_move(String worldId, String move)
	 * 
	 * Result:
	 * State":{"x":"0","y":1}}
	 * 
	 * move = {N, S, E, W}
	 */
	static String make_move(String worldId, String move) throws IOException {
		OkHttpClient client = new OkHttpClient().newBuilder()
				.build();
		MediaType mediaType = MediaType.parse("application/x-www-form-urlencoded");
		RequestBody body = new MultipartBody.Builder().setType(MultipartBody.FORM)
				.addFormDataPart("type", "move")
				.addFormDataPart("teamId", teamId)
				.addFormDataPart("move", move)
				.addFormDataPart("worldId", worldId)
				.build();
		Request request = new Request.Builder()
				.url("https://www.notexponential.com/aip2pgaming/api/rl/gw.php")
				.method("POST", body)
				.addHeader("userId", userId)
				.addHeader("x-api-key", "05049c9e31fc51cdb173")
				.addHeader("Content-Type", "application/x-www-form-urlencoded")
				.build();
		Response response = client.newCall(request).execute();
		// System.out.println(response.body().string());


				// holds the response from the API call
		String jsonResponse = response.body().string();

		// Accessing the JSON values within the response string using the jsonNOde
		// object
		ObjectMapper objectMapper = new ObjectMapper();
		JsonNode jsonNode = objectMapper.readTree(jsonResponse);

		String code = jsonNode.get("code").asText();

		if (code.equals("FAIL")) {
			try {
				String message = jsonNode.get("message").asText();
				System.out.println("FAIL: make_move(), Message: " + message);
			} catch (Exception e) {
				System.out.println("FAIL: make_move()");
			}
			return "-1";
		} else if (code.equals("OK")) {
			String state = jsonNode.get("State").asText();
			System.out.println("Move " + move + " Successful for teamId " + teamId + ". Current State: " + state);
			return "1";
		} else {
			System.out.println("Unknown Error: make_move()");
			return "-1";
		}
	}


	///////////////////
	// GET API CALLS //
	///////////////////

	/*
	 * get_location()
	 * 
	 * API call returns:
	 * {"code":"OK","world":"","state":""}
	 * 
	 * function returns String state
	 */
	static String get_location() throws IOException {
		OkHttpClient client = new OkHttpClient().newBuilder()
				.build();
		Request request = new Request.Builder()
				.url("https://www.notexponential.com/aip2pgaming/api/rl/gw.php?type=location&teamId=1387")
				.method("GET", null)
				.addHeader("userId", userId)
				.addHeader("x-api-key", "05049c9e31fc51cdb173")
				.addHeader("Content-Type", "application/x-www-form-urlencoded")
				.build();
		Response response = client.newCall(request).execute();
		// System.out.println(response.body().string());

		// holds the response from the API call
		String jsonResponse = response.body().string();

		// Accessing the JSON values within the response string using the jsonNOde
		// object
		ObjectMapper objectMapper = new ObjectMapper();
		JsonNode jsonNode = objectMapper.readTree(jsonResponse);

		String code = jsonNode.get("code").asText();

		if (code.equals("FAIL")) {
			try {
				String message = jsonNode.get("message").asText();
				System.out.println("FAIL: get_location(), Message: " + message);
			} catch (Exception e) {
				System.out.println("FAIL: get_location()");
			}
			return "-1";
		} else if (code.equals("OK")) {
			String state = jsonNode.get("state").asText();
			System.out.println(
					"Team " + teamId + " is in World " + jsonNode.get("world").asText() + " and State " + state);
			return state;
		} else {
			System.out.println("Unknown Error: get_location()");
			return "-1";
		}
	} // get_location()

	/*
	 * get_learning_score()
	 * 
	 * Returns:
	 * {"score":#,"code":"OK"}
	 */
	static String get_learning_score() throws IOException {
		OkHttpClient client = new OkHttpClient().newBuilder()
				.build();
		Request request = new Request.Builder()
				.url("https://www.notexponential.com/aip2pgaming/api/rl/score.php?type=score&teamId=1387")
				.method("GET", null)
				.addHeader("userId", userId)
				.addHeader("x-api-key", "05049c9e31fc51cdb173")
				.addHeader("Content-Type", "application/x-www-form-urlencoded")
				.build();
		Response response = client.newCall(request).execute();
		// System.out.println(response.body().string());

		// holds the response from the API call
		String jsonResponse = response.body().string();

		// Accessing the JSON values within the response string using the jsonNOde
		// object
		ObjectMapper objectMapper = new ObjectMapper();
		JsonNode jsonNode = objectMapper.readTree(jsonResponse);

		String code = jsonNode.get("code").asText();

		if (code.equals("FAIL")) {
			try {
				String message = jsonNode.get("message").asText();
				System.out.println("FAIL: get_learning_score(), Message: " + message);
			} catch (Exception e) {
				System.out.println("FAIL: get_learning_score()");
			}
			return "-1";
		} else if (code.equals("OK")) {
			String score = jsonNode.get("score").asText();
			System.out.println("Learning Score: " + score);
			return score;
		} else {
			System.out.println("Unknown Error: learning_score()");
			return "-1";
		}

	} // get_learning_score()

	/*
	 * get_last_x_runs()
	 * 
	 * Return format:
	 * {"runs":[{"runId":"44028","teamId":"1387","gworldId":"0",
	 * "createTs":"2023-04-18 12:50:26","score":"-718.8261978930808","moves":"26"},
	 * ... , ...],"code":"OK"}
	 */
	static List <Run> get_last_x_runs(String x) throws IOException {

		// Create a list to store the array elements
		List<String> myArray = new ArrayList<>();

		OkHttpClient client = new OkHttpClient().newBuilder()
				.build();
		Request request = new Request.Builder()
				.url("https://www.notexponential.com/aip2pgaming/api/rl/score.php?type=runs&teamId=1387&count=1")
				.method("GET", null)
				.addHeader("userId", userId)
				.addHeader("x-api-key", "05049c9e31fc51cdb173")
				.addHeader("Content-Type", "application/x-www-form-urlencoded")
				.build();
		Response response = client.newCall(request).execute();
		System.out.println(response.body().string());

		// holds the response from the API call
		String jsonResponse = response.body().string();

		// Accessing the JSON values within the response string using the jsonNOde object
		ObjectMapper objectMapper = new ObjectMapper();
		JsonNode jsonNode = objectMapper.readTree(jsonResponse);

		String code = jsonNode.get("code").asText();

		List<Run> run_list = new ArrayList<> ();

		if (code.equals("FAIL"))
		{
		String errorMessage = jsonNode.get("message").asText();
		System.out.println("FAIL: " + errorMessage);
		return null;
		}
		else if (code.equals("OK"))
		{
			JsonNode movesNode = jsonNode.path("runs");

			for (JsonNode moveNode : movesNode) {
				String moveId = moveNode.path("runId").asText();
				String teamId = moveNode.path("teamId").asText();
				String gworldId = moveNode.path("gworldId").asText();
				String createTs = moveNode.path("createTs").asText();
				String score = moveNode.path("score").asText();
				String moves = moveNode.path("moves").asText();
				Run runObj = new Run(moveId, teamId, gworldId, createTs, score, moves);
				run_list.add(runObj);
			}
			return run_list;
		}
		else
		{
			System.out.println("Unknown Error" );
			myArray.add("-1");
			return null;
		}
	} // get_last_x_runs()

	/*
	 * reset()
	 * 
	 * Return:
	 * {"code":"OK","teamId":1387}
	 */
	static String reset() throws IOException {
		OkHttpClient client = new OkHttpClient().newBuilder()
				.build();
		MediaType mediaType = MediaType.parse("application/x-www-form-urlencoded");
		Request request = new Request.Builder()
				.url("https://www.notexponential.com/aip2pgaming/api/rl/reset.php?teamId=1387&otp=5712768807")
				.method("GET", null)
				.addHeader("userId", userId)
				.addHeader("x-api-key", "05049c9e31fc51cdb173")
				.addHeader("Content-Type", "application/x-www-form-urlencoded")
				.build();
		Response response = client.newCall(request).execute();
		//System.out.println(response.body().string());

				// holds the response from the API call
		String jsonResponse = response.body().string();

		// Accessing the JSON values within the response string using the jsonNOde
		// object
		ObjectMapper objectMapper = new ObjectMapper();
		JsonNode jsonNode = objectMapper.readTree(jsonResponse);

		String code = jsonNode.get("code").asText();

		if (code.equals("FAIL")) {
			try {
				String message = jsonNode.get("message").asText();
				System.out.println("FAIL: reset(), Message: " + message);
			} catch (Exception e) {
				System.out.println("FAIL: reset()");
			}
			return "-1";
		} else if (code.equals("OK")) {
			System.out.println("Reset Successful for teamId " + teamId);
			return "1";
		} else {
			System.out.println("Unknown Error: reset()");
			return "-1";
		}
	} // reset()

}
