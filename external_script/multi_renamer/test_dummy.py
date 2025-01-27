import os


FILE_COUNT = 2000


if __name__ == '__main__':
    home_path = os.path.expanduser( '~' )
    test_dir = os.path.join( home_path, 'test_rename')

    if not os.path.exists( test_dir ):
        os.makedirs( test_dir )
    
    count = 0
    for idx in range(FILE_COUNT):
        test_file = os.path.basename( test_dir ) + '.' + str(idx).zfill(4) + '.' + 'jpg'
        file_path = os.path.join( home_path, test_dir, test_file)

        with open( file_path, 'w' )as file:
            file.write('')
        
        count += 1

    print('test file make done')