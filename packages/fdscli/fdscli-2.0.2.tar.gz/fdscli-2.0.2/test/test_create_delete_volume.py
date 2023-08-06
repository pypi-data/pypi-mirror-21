'''
Created on Apr 9, 2015

@author: nate
'''
import mock_functions
from mock import patch
from test.base_cli_test import BaseCliTest


class VolumeTest1( BaseCliTest ):
    '''
    This test class handles listing volumes and creating/deleting volumes
    '''
    
    @patch( "fdscli.services.volume_service.VolumeService.list_volumes", side_effect=mock_functions.listVolumes )
    def test_listVolumes(self, mockService ):
        
        args = ["volume", "list", "-format=json"]
        
        print("Making call: volume list -format=json")

        self.cli.run( args )
         
        self.callMessageFormatter(args)
         
        assert mockService.call_count == 1
        
        print("test_listVolumes passed.\n\n")


    @patch( "fdscli.services.volume_service.VolumeService.list_volumes", side_effect=mock_functions.listNoVolumes )
    def test_listVolumes_none(self, mockList ):
        '''
        Test if there are no volumes to list
        '''
        
        args = ["volume", "list"]
        
        self.callMessageFormatter(args)
        self.cli.run( args )
        
        assert mockList.call_count == 1

    @patch( "fdscli.services.volume_service.VolumeService.list_volumes", side_effect=mock_functions.errorGen )
    def test_listVolumesError(self, mockList ):
        '''
        Test what happens when list volumes gets an error
        '''
        
        args = ["volume", "list"]
        
        self.callMessageFormatter(args)
        
        exception = None
        
        try:
            self.cli.run(args)
        except SystemExit as se:
            exception = se
            
        assert exception != None, "Expected to get an exception but got none."
    
    @patch( "fdscli.plugins.volume_plugin.VolumePlugin.pretty_print_volume", side_effect=mock_functions.empty_one)
    @patch( "fdscli.services.response_writer.ResponseWriter.writeTabularData", side_effect=mock_functions.empty_one)        
    @patch( "fdscli.services.response_writer.ResponseWriter.prep_volume_for_table", side_effect=mock_functions.empty_two )
    @patch( "fdscli.services.volume_service.VolumeService.get_volume", side_effect=mock_functions.getVolume )
    def test_get_volume(self, mockService, mockPrep, mockTabular, mockPretty ):
        
        args = ["volume", "list", "-volume_id", "3"]
        
        print("Making call: volume list -volume_id 3")

        self.cli.run( args )
         
        self.callMessageFormatter(args)
         
        assert mockService.call_count == 1

        assert mockPrep.call_count == 0
        
        print("test_get_volume passed.\n\n")
        
    @patch( "fdscli.plugins.volume_plugin.VolumePlugin.pretty_print_volume", side_effect=mock_functions.empty_one)
    @patch( "fdscli.services.response_writer.ResponseWriter.writeTabularData", side_effect=mock_functions.empty_one)
    @patch( "fdscli.services.response_writer.ResponseWriter.prep_volume_for_table", side_effect=mock_functions.empty_two )
    @patch( "fdscli.services.volume_service.VolumeService.get_volume", side_effect=mock_functions.getVolume )
    def test_get_volume_failure(self, mockService, mockPrep, mockTabular, mockPretty ):
        
        #the side effect method here will only be successful for a 3
        args = ["volume", "list", "-volume_id", "2"]
        
        print("Making call: volume list -volume_id 2")
        
        exception = None

        try:
            self.cli.run( args )
        except SystemExit as se:
            exception = se;
         
        self.callMessageFormatter(args)
         
        assert exception != None, "Expected a SystemExit to be raised but it didn't happen"
        assert mockService.call_count == 1
        assert mockPrep.call_count == 0, "Expected the volume preparation method not to be called."
        assert mockTabular.call_count == 0, "Expected the volume write table method not to be called."
        
        print("test_get_volume_failure passed.\n\n")        

    @patch( "fdscli.services.volume_service.VolumeService.list_volumes", side_effect=mock_functions.listVolumes )
    @patch( "fdscli.services.volume_service.VolumeService.delete_volume", side_effect=mock_functions.deleteVolume )
    def test_deleteVolume_by_id(self, mockDelete, listCall ):
        
        args = ["volume", "delete", "-volume_id=3" ]
        
        self.callMessageFormatter(args)
        
        self.cli.run( args )
        
        assert mockDelete.call_count == 1
        
        v_id = mockDelete.call_args[0][0]
        
        print("Making sure we call the find method with the ID and get a certain name to the delete call.")

        assert v_id == "3"
        
    @patch( "fdscli.services.volume_service.VolumeService.list_volumes", side_effect=mock_functions.listVolumes )
    @patch( "fdscli.services.volume_service.VolumeService.delete_volume", side_effect=mock_functions.deleteVolume )
    def test_deleteVolume_by_name(self, mockDelete, listCall ):
        
        args = ["volume", "delete", "-volume_name=FakeVol" ]
        
        self.callMessageFormatter(args)
        
        self.cli.run( args )
        
        assert mockDelete.call_count == 1
        
        v_id = mockDelete.call_args[0][0]
        
        print("Making sure we call the find method with the name and get a certain ID to the delete call.")

        assert v_id == 1        


    @patch( "fdscli.services.volume_service.VolumeService.list_volumes", side_effect=mock_functions.listVolumes )
    @patch( "fdscli.services.volume_service.VolumeService.create_volume", side_effect=mock_functions.createVolume )
    def test_create_with_defaults(self, volumeCreateMethod, listCall):

        args = ["volume", "create", "object", "-name=Franklin"]

        self.callMessageFormatter(args)
      
        self.cli.run( args )
        
        assert volumeCreateMethod.call_count == 1
        
        volume = volumeCreateMethod.call_args[0][0]
        
        print("Checking the call stack to make sure it went to the right place")

        assert volume.data_protection_policy.commit_log_retention == 86400
        assert volume.id == -1
        assert volume.name == "Franklin"
        assert volume.qos_policy.iops_min == 0
        assert volume.qos_policy.iops_max == 0
        assert volume.media_policy == "HYBRID"
        assert volume.qos_policy.priority == 7
        assert volume.settings.type == "OBJECT"
        assert volume.settings.encryption == False
        assert volume.settings.compression == False
        
        print("test_create_with_defaults passed.\n\n")

    @patch( "fdscli.services.volume_service.VolumeService.list_volumes", side_effect=mock_functions.listVolumes )
    @patch( "fdscli.services.volume_service.VolumeService.create_volume", side_effect=mock_functions.createVolume )        
    def test_create_with_size(self, volumeCreate, listCall ):
        ''' 
        testing PB
        '''
        
        args = [ "volume", "create", "iscsi", "-name", "whoop", "-size", "4", "-size_unit", "PB"]
        
        self.callMessageFormatter(args)
        self.cli.run( args )
         
        volume = volumeCreate.call_args[0][0]
        
        assert volume.name == "whoop"
        assert volume.settings.type == "ISCSI"
        assert volume.settings.capacity.size == 4
        assert volume.settings.capacity.unit == "PB"

    @patch( "fdscli.services.volume_service.VolumeService.list_volumes", side_effect=mock_functions.listVolumes )
    @patch( "fdscli.services.volume_service.VolumeService.create_volume", side_effect=mock_functions.createVolume )
    def test_create_with_args(self, volumeCreate, listCall):
        '''
        Parameters
        ----------
        volumeCreate (unittest.mock.MagicMock)
        listCall (unittest.mock.MagicMock)
        '''
        args = ["volume", "create", "iscsi", "-name=Franklin2", "-priority=1", "-iops_min=30", "-iops_max=30", "-continuous_protection=86400",
                "-tiering_policy=SSD", "-size=2", "-size_unit=MB", "-encryption", "true", "-compression", "true"]
         
        self.callMessageFormatter(args)
        self.cli.run( args )
        volume = volumeCreate.call_args[0][0]
         
        print("Checking the parameters made it through")

        assert volume.data_protection_policy.commit_log_retention == 86400
        assert volume.id == -1
        assert volume.name == "Franklin2"
        assert volume.qos_policy.iops_min == 30
        assert volume.qos_policy.iops_max == 30
        assert volume.media_policy == "SSD"
        assert volume.qos_policy.priority == 1
        assert volume.settings.type == "ISCSI"
        assert volume.status.current_usage.size == 0
        assert volume.status.current_usage.unit == "GB"   
        assert volume.settings.encryption == True
        assert volume.settings.compression == True

        print("test_create_with_args passed.\n\n")

    @patch( "fdscli.services.volume_service.VolumeService.create_volume", side_effect=mock_functions.createVolume )
    def test_create_boundary_checking(self, volumeCreate):

        args = ["volume", "create", "nfs", "-name=Franklin2", "-priority=11", "-iops_min=30", "-iops_max=30",
                "-continuous_protection=86400", "-tiering_policy=SSD", "-size=2", "-size_unit=PB"]

        self.callMessageFormatter(args)
        print("Testing bad volume type")
        args[2] = "abcd"
        self.cli.run( args )
        assert volumeCreate.call_count == 0

        print("Testing bad priority")
        self.cli.run( args )
        args[2] = "nfs"
        assert volumeCreate.call_count == 0

        print("Testing bad iops_guarantee")
        args[4] = "-priority=1"
        args[5] = "-iops_min=-1"
        self.cli.run(args)
        assert volumeCreate.call_count == 0

        print("Testing bad iops_limit")
        args[5] = "-iops_min=4000"
        args[6] = "-iops_max=100000"
        self.cli.run(args)
        assert volumeCreate.call_count == 0

        print("Testing bad continuous protection")
        args[6] = "-iops_max=1000"
        args[7] = "-continuous_protection=-1"
        self.cli.run( args )
        assert volumeCreate.call_count == 0

        print("Testing bad media policy")
        args[7] = "-continuous_protection=86400"
        args[8] = "-tiering_policy=MY_POLICY"
        self.cli.run( args )
        assert volumeCreate.call_count == 0

        print("Testing bad block size")
        args[8] = "-tiering_policy=SSD"
        args[9] = "-size=-1"
        self.cli.run( args )
        assert volumeCreate.call_count == 0

        print("Testing bad units")
        args[9] = "-size=2"
        args[10] = "-size_unit=EB"
        self.cli.run( args )
        assert volumeCreate.call_count == 0
        print("test_create_boundary_checking passed.\n\n")
