//SORTSDK1 JOB (113200000),'PETR VACULA',MSGCLASS=A,CLASS=A,
//            MSGLEVEL=(1,1),NOTIFY=&SYSUID
//STEP010  EXEC PGM=SORT
//SYSOUT   DD SYSOUT=*
//SORTIN   DD DSN=PUBLIC.MFTSTAUT.ROBOT.SORTSDK1,DISP=SHR
//SORTOUT  DD SYSOUT=*
//SYSIN    DD *
 SORT FIELDS=(1,10,CH,A)
/*
//