package com.psupozyx.app;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

import java.io.IOException;

public class Main extends Application {
    private Parent root;

    @Override
    public void start(Stage primaryStage) throws Exception{
        root = FXMLLoader.load(getClass().getClassLoader().getResource("fxml/layout_main.fxml"));
        primaryStage.setTitle("PSU Pozyx");
        primaryStage.setScene(new Scene(root, 1024, 768));
        primaryStage.show();
    }


    public static void main(String[] args) {
        launch(args);
    }

    void openStage(String fxmlPath, String title, int width, int height) {
        try {
            root = FXMLLoader.load(getClass().getClassLoader().getResource(fxmlPath));
        } catch (IOException e) {
            e.printStackTrace();
        }
        Stage newStage = new Stage();
        newStage.setTitle(title);
        newStage.setScene(new Scene(root, width, height));
        newStage.show();
    }
}
