package com.harry.test;

import com.harry.bean.Student;
import com.harry.dao.Impl.StudentDaoImpl;
import com.harry.dao.StudentDao;
import org.junit.Test;

public class StudentTest01 {

    @Test
    public void insertStudent(){
        StudentDao studentDao = new StudentDaoImpl();
        Student student = new Student("刘德华", 52, 98.50);

        studentDao.insertStudent(student);
    }
}