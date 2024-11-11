package dev.algo.ageit.accounting;

import org.eclipse.swt.widgets.Display;

public class Main {
    public static void main(String[] args) {
        Display display = new Display();
        MainWindow window = new MainWindow(display);
        window.open();

        while (!window.isDisposed()) {
            if (!display.readAndDispatch()) {
                display.sleep();
            }
        }
        display.dispose();
    }
}