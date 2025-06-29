一 什么进程
	进程是当一个静态的程序启动之后称之为一个进程。而负责执行是CPU。
	也就是说程序只一堆静态的代码，当程序被运行起来后才可以称之为是一个进程
	
二 并发与并行
	无论是并发还是并行在用户看来都是同时执行，主要区别在于多颗CPU是否同时运行一个任务还是一颗CPU在多个任务之间来回切换
	1 并发：是伪并行 即看起来是在同时运行，但是单颗CPU会在多个任务之间快速的切换
	2 并行：同时运行，多颗CPU同时工作，每个CPU都运行用一个任务，操作系统会将这些任务调度到不同的cpu上运行   
	
	
三 进程的创建（了解）
	但凡是硬件，都需要有操作系统去管理，只要有操作系统，就有进程的概念，就需要有创建进程的方式，一些操作系统只为一个应用程序设计，比如微波炉中的控制器，一旦启动微波炉，所有的进程都已经存在。
	而对于通用系统（跑很多应用程序），需要有系统运行过程中创建或撤销进程的能力，主要分为4中形式创建新的进程
	系统初始化（查看进程linux中用ps命令，windows中用任务管理器，前台进程负责与用户交互，后台运行的进程与用户无关，运行在后台并且只在需要时才唤醒的进程，称为守护进程，如电子邮件、web页面、新闻、打印）
	一个进程在运行过程中开启了子进程（如nginx开启多进程，os.fork,subprocess.Popen等）
	用户的交互式请求，而创建一个新进程（如用户双击暴风影音）
	一个批处理作业的初始化（只在大型机的批处理系统中应用）
	无论哪一种，新进程的创建都是由一个已经存在的进程执行了一个用于创建进程的系统调用而创建的：
	在UNIX中该系统调用是：fork，fork会创建一个与父进程一模一样的副本，二者有相同的存储映像、同样的环境字符串和同样的打开文件（在shell解释器进程中，执行一个命令就会创建一个子进程）
	在windows中该系统调用是：CreateProcess，CreateProcess既处理进程的创建，也负责把正确的程序装入新进程。
	关于创建的子进程，UNIX和windows
	1.相同的是：进程创建后，父进程和子进程有各自不同的地址空间（多道技术要求物理层面实现进程之间内存的隔离），任何一个进程的在其地址空间中的修改都不会影响到另外一个进程。
	2.不同的是：在UNIX中，子进程的初始地址空间是父进程的一个副本，提示：子进程和父进程是可以有只读的共享内存区的。但是对于windows系统来说，从一开始父进程与子进程的地址空间就是不同的。
	
四 Python中开启进程的两种方式
	Python提供了multiprocessing。 multiprocessing模块用来开启子进程，并在子进程中执行我们定制的任务（比如函数），该模块与多线程模块threading的编程接口类似。
	multiprocessing模块的功能众多：支持子进程、通信和共享数据、执行不同形式的同步，>提供了Process、Queue、Pipe、Lock等组件。
	1 process类介绍
		Process([group [, target [, name [, args [, kwargs]]]]])，由该类实例化得到的对象，可用来开启一个子进程
		参数介绍：
			group参数未使用，值始终为None
			target表示调用对象，即子进程要执行的任务
			args表示调用对象的位置参数元组，args=(1,2,'egon',) 注意 元祖中必须加逗号
			kwargs表示调用对象的字典,kwargs={'name':'egon','age':18}
			name为子进程的名称
		方法介绍	
			p.start()：启动进程，并调用该子进程中的p.run() 
			p.run():进程启动时运行的方法，正是它去调用target指定的函数，我们自定义类的类中一定要实现该方法  
			p.terminate():强制终止进程p，不会进行任何清理操作，如果p创建了子进程，该子进程就成了僵尸进程，使用该方法需要特别小心这种情况。如果p还保存了一个锁那么也将不会被释放，进而导致死锁
			p.is_alive():如果p仍然运行，返回True
			p.join([timeout]):主线程等待p终止（强调：是主线程处于等的状态，而p是处于运行的状态）。timeout是可选的超时时间。
		属性介绍：
			p.daemon：默认值为False，如果设为True，代表p为后台运行的守护进程，当p的父进程终止时，p也随之终止，并且设定为True后，p不能创建自己的新进程，必须在p.start()之前设置
			p.name:进程的名称
			p.pid：进程的pid	
		代码：
			from mulitiprocessing import process
			def multProcess(name):
				print(name)
			p = mulitiprocessing.process(target=multiProcess, args=(('harry'))
			p.start()
    2 使用类的方式创建子进程
		class myProcess(process):
			super().__init__()
			def __init__(self, name):
				self.name = name
			def run(self)
				print(self.name)
		
		p1 = myProcess('harry')
		p1.start()         # 此时进程会运行类中的run方法
	3 几个练习题
	   (1) 进程之间的内存空间是共享的还是隔离的？下述代码的执行结果是什么？
			进程之间的内存空间是隔离的，下面这段代码主进程的n是100 子进程为0
			from multiprocessing import Process
			n=100 #在windows系统中应该把全局变量定义在if __name__ == '__main__'之上就可以了
			def work():
				global n
				n=0
				print('子进程内: ',n)

			if __name__ == '__main__':
				p=Process(target=work)
				p.start()
				print('主进程内: ',n)
	   (2)	基于多进程实现套接字通信
			from multiprocessing import Process
			import socket
			def create_socket():
				sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sk.bind(('127.0.0.1', 8080))
				sk.listen()
				return sk

			def talk(conn):
				while True:
					try:
						data = conn.recv()
						if not data:break
						conn.send(data)
					except Exception:
						break
				
			def connect():
				while True:
					sk = create_socket()
					conn, addr = sk.accept()
					p = Process(target=talk, args=(conn,))
					p.start()
			if __name__ == '__main__':
				connect()

五 Process的join方法
	1 join方法简介
		当一个主进程开启了多个子进程时，主进程与进程会同时执行，但是如果想要等某个进程运行完毕之后再运行主进程那么就用到了join方法。
		使用join方法后如果子进程没有运行完成那么主进程会一直处于阻塞状态直到子进程运行完毕才会继续运行
	2 代码：
		from multiprocessing import Process
		import time
		import random

		def task(name):
			print('%s is piaoing' %name)
			time.sleep(random.randint(1,3))
			print('%s is piao end' %name)

		if __name__ == '__main__':
			p1=Process(target=task,args=('cs',))
			p2=Process(target=task,args=('alex',))
			p3=Process(target=task,args=('harry',))
			p4=Process(target=task,args=('jerry',))

			p1.start()
			p2.start()
			p3.start()
			p4.start()
			
			p1.join()
			p2.join()
			p3.join()
			p4.join()

			print('主')
			
六 守护进程
	当一个子进程开启守护进程后那么它将会守护着主进程，如果主进程一旦接受那么守护进程也就随之结束
	代码：
		from multiprocessing import Process
		import time
		import random

		def task(name):
			print('%s is piaoing' %name)
			time.sleep(random.randrange(1,3))
			print('%s is piao end' %name)


		if __name__ == '__main__':
			p=Process(target=task,args=('egon',))
			p.daemon=True #一定要在p.start()前设置,设置p为守护进程,禁止p创建子进程,并且父进程代码执行结束,p即终止运行
			p.start()
			print('主') #只要终端打印出这一行内容，那么守护进程p也就跟着结束掉了
			
七 互斥锁
	当多个子进程去同时取一个共享数据时可能会造成数据的混乱，互斥锁的作用就是当一个进程去拿数据时会将其他进程锁在门外，知道这个进程处理完成之后才放入其他进程，
	这样就可以避免了进程之间竞争造成的数据混乱
	#由并发变成了串行,牺牲了运行效率,但避免了竞争
		from multiprocessing import Process,Lock
		import os,time
		def work(lock):
			lock.acquire() #加锁
			print('%s is running' %os.getpid())
			time.sleep(2)
			print('%s is done' %os.getpid())
			lock.release() #释放锁
		if __name__ == '__main__':
			lock=Lock()
			for i in range(3):
				p=Process(target=work,args=(lock,))
				p.start()
				
	def task(name, lock):
		lock.acquire()
		print('%s 1'%name)
		time.sleep(1)
		print('%s 2' %name)
		time.sleep(1)
		print('%s 3' %name)
		lock.release()
	if __name__ == '__main__':
		lock = RLock()
		for i in range(3):
			p = Process(target=task, args=('主进程%s'%i, lock,))
			p.start()
	
	模拟抢票案例
		import json
		import time
		from multiprocessing import Process, Lock
		def search(name):
			time.sleep(1)
			dic = json.load(open('db.txt', 'r', encoding='utf-8'))
			print('<%s> 查看到剩余票数 %s' %(name,dic['count']))

		def get(name):
			time.sleep(1)
			dic = json.load(open('db.txt', 'r', encoding='utf-8'))
			if dic['count'] > 0:
				dic['count']-=1
				time.sleep(3)
				json.dump(dic, open(('db.txt'), 'w', encoding='utf-8'))
				print('<%s>购票成功 '%name)
		def task(name, mutex):
			search(name)
			mutex.acquire()
			get(name)
			mutex.release()
		if __name__ == '__main__':
			mutex = Lock()
			for i in range(10):
				p = Process(target=task, args=('路人%s' %i, mutex,))
				p.start()
				
八 队列实现进程间通信
	1 队列介绍
		在多进程中，各个进程之间的数据是互相隔离的，要实现进程间通信(IPC),multiprocessing模块支持两种形式：队列和管道，这两种方式都是使用消息传递的
		创建队列的类：Queue([maxsize]):创建共享的进程队列，Queue是多进程安全的队列，可以使用Queue实现多进程之间的数据传递。
	2 参数介绍：
		maxsize是队列中允许最大项数，省略则无大小限制。
		但需要明确：
			1、队列内存放的是消息而非大数据
			2、队列占用的是内存空间，因而maxsize即便是无大小限制也受限于内存大小
	3 主要方法介绍
		q.put方法用以插入数据到队列中。
			put方法还有两个可选参数：blocked和timeout。如果blocked为True（默认值），并且timeout为正值，该方法会阻塞timeout指定的时间，直到该队列有剩余的空间。如果超时，会抛出Queue.Full异常。如果blocked为False，但该Queue已满，会立即抛出Queue.Full异常。
        q.get方法可以从队列读取并且删除一个元素。
			同样，get方法有两个可选参数：blocked和timeout。如果blocked为True（默认值），并且timeout为正值，那么在等待时间内没有取到任何元素，会抛出Queue.Empty异常。如果blocked为False，有两种情况存在，如果Queue有一个值可用，则立即返回该值，否则，如果队列为空，则立即抛出Queue.Empty异常
	4 生产者消费者模型
		什么是生产者和消费者模型
		生产者消费者模式通过一个容器来解决生产者和消费者之前的强耦合问题。生产者和消费者之间不直接通讯，
		而通过队列来进行通讯，所有生产者生成数据之后不用等待消费者处理直接塞给队列，消费者不找生产者要数据而是直接从阻塞队列里取
		阻塞队列相当于一个缓冲区，平衡了生产者和消费者的处理能力
		
		为什么使用生产者消费者模型
		生产者指的是生产数据的任务，消费者指的是处理数据的任务，在并发编程中，如果生产者处理速度很快，而消费者处理速度很慢，那么生产者就必须等待消费者处理完，才能继续生产数据。
		同样的道理，如果消费者的处理能力大于生产者，那么消费者就必须等待生产者。为了解决这个问题于是引入了生产者和消费者模式。
		
		示例一： 造成结果，如果生产者生产完包子，消费者哪个不到包子会导致程序一直进入阻塞状态
			from multiprocessing import  Process
			from multiprocessing import Queue
			import time
			import random

			def producer(q):
				for i in range(3):
					print('开始做包子了')
					num = random.randint(0,99)
					q.put(num)
					time.sleep(1)
					print('包子%s好了'%num)

			def consume(q):
				while True:
					res = q.get()
					if res is None:break
					time.sleep(2)
					print('吃包子%s'%res)

			if __name__ == '__main__':
					q = Queue()
					producer_process = Process(target=producer,args=(q,))
					consumer_process = Process(target=consume, args=(q,))
					producer_process.start()
					consumer_process.start()
		示例二： 根据示例一造成的结果可以在producer的进程执行完成后在主进程put一个None
			from multiprocessing import  Process
			from multiprocessing import Queue
			import time
			import random

			def producer(q):
				for i in range(3):
					print('开始做包子了')
					num = random.randint(0, 99)
					q.put(num)
					time.sleep(random.randint(1, 3))
					print('包子%s好了' % num)

			def consume(q):
				while True:
					res = q.get()
					if res is None:break

					time.sleep(random.randint(1,3))
					print('吃包子%s' % res)
			if __name__ == '__main__':
					q = Queue()
					producer_process = Process(target=producer,args=(q,))
					consumer_process = Process(target=consume, args=(q,))
					producer_process.start()
					consumer_process.start()
					producer_process.join()
					q.put(None)
		示例三：如果有多个消费者时那么在主进程中就需要put与消费者相等的None这种写法太过low，我们可以通过JoinableQueue来实现	
		JoinableQueue的实例p除了与Queue对象相同的方法之外还具有：
		q.task_done()：使用者使用此方法发出信号，表示q.get()的返回项目已经被处理。如果调用此方法的次数大于从队列中删除项目的数量，将引发ValueError异常
		q.join():生产者调用此方法进行阻塞，直到队列中所有的项目均被处理。阻塞将持续到队列中的每个项目均调用q.task_done（）方法为止
		注意：
		 #1、主进程等生产者p1、p2、p3结束
		 #2、而p1、p2、p3是在消费者把所有数据都取干净之后才会结束
         #3、所以一旦p1、p2、p3结束了，证明消费者也没必要存在了，应该随着主进程一块死掉，因而需要将生产者们设置成守护进程
			from multiprocessing import Process,JoinableQueue
			import time
			import random

			def producer(q,name):
				print('开始做包子了')
				for i in range(3):
					time.sleep(random.randint(1, 3))
					num = random.randint(0, 99)
					q.put(num)
					print('%s做好包子%s了' %(name, num))
				q.join() # 等到消费者把自己放入队列中的所有的数据都取走之后，生产者才结束


			def consume(q,name):
				while True:
					res = q.get()
					if res is None:break
					time.sleep(random.randint(1,3))
					print('%s吃包子%s' %(name,res))
					q.task_done()  # 发送信号给q.join()，说明已经从队列中取走一个数据并处理完毕了

			if __name__ == '__main__':
					q = JoinableQueue()
					p1 = Process(target=producer,args=(q, '厨师1',))
					p2 = Process(target=producer,args=(q, '厨师2',))
					p3 = Process(target=producer,args=(q, '厨师3',))
					c1 = Process(target=consume, args=(q, '顾客1',))
					c2 = Process(target=consume, args=(q, '顾客2',))
					c3 = Process(target=consume, args=(q, '顾客3',))

					c1.daemon = True
					c2.daemon = True
					c3.daemon = True

					p1.start()
					p2.start()
					p3.start()

					c1.start()
					c2.start()
					c3.start()

					p1.join()
					p2.join()
					p3.join()
					print('主')

九 进程池
	一个操作系统无法无限制的开启进程，因为进程会大量的消耗系统的资源，进程开启的过多反而会导致效率下降，
	因此我们可以通过维护一个进程池来控制进程数目，比如httpd进程模式规定最小进程和最大进程数
	创建进程池的类：如果指定numprocess为3，则进程池会从无到有创建三个进程，然后自始至终使用这三个进程去执行所有任务，不会开启其他进程
		Pool([numprocess  [,initializer [, initargs]]]):创建进程池
	参数介绍：
		1 numprocess:要创建的进程数，如果省略，将默认使用cpu_count()的值
		2 initializer：是每个工作进程启动时要执行的可调用对象，默认为None
		3 initargs：是要传给initializer的参数组
	方法介绍
		1 p.apply(func [, args [, kwargs]]):在一个池工作进程中执行func(*args,**kwargs),然后返回结果。需要强调的是：此操作并不会在所有池工作进程中并执行func函数。如果要通过不同参数并发地执行func函数，必须从不同线程调用p.apply()函数或者使用p.apply_async()
		2 p.apply_async(func [, args [, kwargs]]):在一个池工作进程中执行func(*args,**kwargs),然后返回结果。此方法的结果是AsyncResult类的实例，callback是可调用对象，接收输入参数。当func的结果变为可用时，将理解传递给callback。callback禁止执行任何阻塞操作，否则将接收其他异步操作中的结果。 
		3 p.close():关闭进程池，防止进一步操作。如果所有操作持续挂起，它们将在工作进程终止前完成
		4 P.jion():等待所有工作进程退出。此方法只能在close（）或teminate()之后调用
		
		示例一： 同步调用
			from multiprocessing import Pool
			import os,time

			def work(n):
				print("%s run" %os.getpid())
				time.sleep(3)
				return n**2

			if __name__ == '__main__':
				p = Pool(3) # 进程池中从无到有创建三个进程，以后一直是这三个进程执行任务
				res_l = []
				for i in range(10):
					res = p.apply(work, args=(i,)) # 同步调用，知道本次任务执行完毕拿到res，等待任务work执行的过程中可能有阻塞也可能没有阻塞，但是不管该任务是否在阻塞，同步调用都会在原地等着，只是等的过程中若是任务发生了阻塞就会被夺走cpu执行权限
					res_l.append(res)

				print(res_l)
		示例二： 异步调用
			
			from multiprocessing import Pool
			import os,time
			def work(n):
				print('%s run' %os.getpid())
				time.sleep(3)
				return n**2

			if __name__ == '__main__':
				p=Pool(3) #进程池中从无到有创建三个进程,以后一直是这三个进程在执行任务
				res_l=[]
				for i in range(10):
					res=p.apply_async(work,args=(i,)) #同步运行,阻塞、直到本次任务执行完毕拿到res
					res_l.append(res)

				#异步apply_async用法：如果使用异步提交的任务，主进程需要使用jion，等待进程池内任务都处理完，然后可以用get收集结果，否则，主进程结束，进程池可能还没来得及执行，也就跟着一起结束了
				p.close()
				p.join()
				for res in res_l:
					print(res.get()) #使用get来获取apply_aync的结果,如果是apply,则没有get方法,因为apply是同步执行,立刻获取结果,也根本无需get
					
十 concurrent.futures模块的线程池与进程池
	与前者类型，这块模块提供的ThreadPoolExecutor和ProcessPoolExecutor也是用于控制最大进程数与线程数
	
	基本方法
		1、submit(fn, *args, **kwargs)
		异步提交任务

		2、map(func, *iterables, timeout=None, chunksize=1) 
		取代for循环submit的操作

		3、shutdown(wait=True) 
		相当于进程池的pool.close()+pool.join()操作
		wait=True，等待池内所有任务执行完毕回收完资源后才继续
		wait=False，立即返回，并不会等待池内的任务执行完毕
		但不管wait参数为何值，整个程序都会等到所有任务执行完毕
		submit和map必须在shutdown之前

		4、result(timeout=None)
		取得结果

		5、add_done_callback(fn)
		
	map用法
		from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor

		import os,time,random
		def task(n):
			print('%s is runing' %os.getpid())
			time.sleep(random.randint(1,3))
			return n**2

		if __name__ == '__main__':

			executor=ThreadPoolExecutor(max_workers=3)

			# for i in range(11):
			#     future=executor.submit(task,i)

			executor.map(task,range(1,12)) #map取代了for+submit	
			
		
	回调函数
	
	异步调用与回调机制
		1 同步调用: 提交完任务后就在原地等待任务执行完毕，拿到结果再指向下一行代码
        2 异步调用: 提交完任务后，不在等待任务执行完毕 
		
		# 同步调用示例 线程池中每个线程都必须拿到返回结果才回执行下面的函数，相当于串行
			def  la(name):
				print('%s is laing' %name)
				time.sleep(random.randint(3,5))
				res = random.randint(7,13)*'#'
				return {'name':name, 'res':res}

			def weight(shit):
				name = shit['name']
				size = len(shit['res'])
				print('%s 拉了 <<%s>>kg' %(name,size))

			if __name__ == '__main__':
				pool = ThreadPoolExecutor(13)
				shit1 = pool.submit(la, 'alex').result()
				weight(shit1)
				shit2 = pool.submit(la, '222').result()
				weight(shit2)
		 
		# 异步调用 提交完任务后，不在等待任务执行完毕可实现并行，当拿到结果后再执行回调函数
			def  la(name):
				print('%s is laing' %name)
				time.sleep(random.randint(3,5))
				res = random.randint(7,13)*'#'
				return ({'name':name, 'res':res})

			def weight(shit):
				shit = shit.result()
				name = shit['name']
				size = len(shit['res'])
				print('%s 拉了 <<%s>>kg' %(name,size))

			if __name__ == '__main__':
				pool = ThreadPoolExecutor(13)
				pool.submit(la, 'alex').add_done_callback(weight)
				pool.submit(la, '333').add_done_callback(weight)
				pool.submit(la, '222').add_done_callback(weight)
