import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

public class ComputeImportance{
	public static void main(String[] args){
		Process p;
		/*利用CMD命令调用python，包含两个参数，一个是有价值的文档集目录路径，一个是新文档的路径*/
		String cmd="python ComputeImportance.py \"D:\\UCAS\\Phd\\Projects\\201805YuGaiHong\\docs\" \"D:\\UCAS\\Phd\\Projects\\201805YuGaiHong\\new.txt\"";
		try{
			p = Runtime.getRuntime().exec(cmd);
			InputStream fis=p.getInputStream();
			InputStreamReader isr=new InputStreamReader(fis);
			BufferedReader br=new BufferedReader(isr);
			String line=br.readLine();/*得到命令行返回的分数值，此时是字符串类型*/
			System.out.println(line);
		}
		catch (IOException e){
			e.printStackTrace();
		}
	}
}