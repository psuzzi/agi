package dev.algo.ageit.accounting;

import org.eclipse.swt.SWT;
import org.eclipse.swt.layout.GridLayout;
import org.eclipse.swt.widgets.*;

public class MainWindow {
    private Display display;
    private Shell shell;

    public MainWindow(Display display) {
        this.display = display;
        createContents();
    }

    private void createContents() {
        shell = new Shell(display);
        shell.setText("SWT Application");
        shell.setLayout(new GridLayout(1, true));

        // Add a sample button
        Button button = new Button(shell, SWT.PUSH);
        button.setText("Click Me!");
        button.addListener(SWT.Selection, event -> {
            MessageBox messageBox = new MessageBox(shell, SWT.ICON_INFORMATION | SWT.OK);
            messageBox.setMessage("Hello, SWT World!");
            messageBox.open();
        });

        shell.pack();
    }

    public void open() {
        shell.open();
    }

    public boolean isDisposed() {
        return shell.isDisposed();
    }
}