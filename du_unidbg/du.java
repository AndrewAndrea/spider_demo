package cn.du;

import com.github.unidbg.AndroidEmulator;
import com.github.unidbg.Module;
import com.github.unidbg.linux.android.AndroidARMEmulator;
import com.github.unidbg.linux.android.AndroidResolver;
import com.github.unidbg.linux.android.dvm.*;
import com.github.unidbg.linux.android.dvm.array.ByteArray;
import com.github.unidbg.memory.Memory;


import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.URL;

//毒app 4.16.0
public class du extends AbstractJni {

//    private static AndroidEmulator createARMEmulator() {
//        return new AndroidARMEmulator("com.xingin.xhs");
//    }

    //ARM模拟器
    private final AndroidEmulator emulator;
    //vm
    private final VM vm;
    //载入的模块
    private final Module module;

    private final DvmClass TTEncryptUtils;

    //初始化
    public du() throws IOException {
        //创建毒进程，这里其实可以不用写的，我这里是随便写的，使用app本身的进程就可以绕过进程检测
//        emulator = new AndroidARMEmulator("com.du.du");
        emulator = new AndroidARMEmulator("com.shizhuang.duapp");
        final Memory memory = emulator.getMemory();
        //作者支持19和23两个sdk
        memory.setLibraryResolver(new AndroidResolver(23));
//        memory.setCallInitFunction();
        //创建DalvikVM，利用apk本身，可以为null
        //如果用apk文件加载so的话，会自动处理签名方面的jni，具体可看AbstractJni,这就是利用apk加载的好处
//        vm = emulator.createDalvikVM(new File("src/test/resources/du/dewu.apk"));
        vm = emulator.createDalvikVM(null);
        vm.setVerbose(true);
        vm.setJni(this);
//        vm = emulator.createDalvikVM(null);
        //加载so，使用armv8-64速度会快很多
        System.out.println("star111t");
        InputStream in = du.class.getClassLoader().getResourceAsStream("du/libJNIEncrypt.so");
        System.out.println(in);
        int index;
        byte[] bytes = new byte[1024];
        FileOutputStream downloadFile = new FileOutputStream("libJNIEncrypt.so");
        while ((index = in.read(bytes)) != -1) {
            downloadFile.write(bytes, 0, index);
            downloadFile.flush();
        }
        in.close();
        downloadFile.close();
//        File file_2 = new File(url_2.getFile());
//        String filepath_2 = file_2.getPath();
        DalvikModule dm = vm.loadLibrary(new File("libJNIEncrypt.so"), false);
        //调用jni
        dm.callJNI_OnLoad(emulator);
        module = dm.getModule();
        //Jni调用的类，加载so
        TTEncryptUtils = vm.resolveClass("com/duapp/aesjni/AESEncrypt");
    }


    //关闭模拟器
    private void destroy() throws IOException {
        emulator.close();
        System.out.println("destroy");
    }

    public static void main(String[] args) throws IOException {
        System.out.println("start");
        du t = new du();
        t.encodeByte("1234324");
        t.destroy();

    }

    public String encodeByte(String strs) {
        //调试
        // 这里还支持gdb调试，
        //emulator.attach(DebuggerType.GDB_SERVER);
        //附加调试器
//        emulator.attach(DebuggerType.SIMPLE);
//        emulator.traceCode();
        //这里是打断点，原地址0x00005028->新地址0x40005028 新地址需要改成0x4
//        emulator.attach().addBreakPoint(null, 0x40001188);//encode地址
//        emulator.attach().addBreakPoint(null, 0x40000D10);
        Number ret = TTEncryptUtils.callStaticJniMethod(emulator, "getByteValues()Ljava/lang/String;");
        System.out.println(ret);
        System.out.println("-----------------------");
        long hash = ret.intValue() & 0xffffffffL;
        StringObject st1 = vm.getObject(hash);
        //*这里要处理下字符串
        String byteString = st1.getValue();
        StringBuilder builder = new StringBuilder(byteString.length());
        for (int i = 0; i < byteString.length(); i++) {
            if (byteString.charAt(i) == '0') {
                builder.append('1');
            } else {
                builder.append('0');
            }
        }
        byte[] strs_byte = strs.getBytes();
        //获取encodeByte地址
        ret = TTEncryptUtils.callStaticJniMethod(emulator, "encodeByte([BLjava/lang/String;)Ljava/lang/String;", vm.addLocalObject(new ByteArray(strs_byte)),

                //传参，这里需要两个字符串，所以就传入两个参数
//                vm.addLocalObject(new StringObject(vm, strs)),
                vm.addLocalObject(new StringObject(vm, builder.toString()))

        );
        //ret 返回的是地址，
        hash = ret.intValue() & 0xffffffffL;
        //获得其值
        StringObject str = vm.getObject(hash);
        System.out.println(str);
        System.out.println("----------------------");
        System.out.println(str.getValue());
        return str.getValue();
    }
}